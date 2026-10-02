# Runtime modules & workers

MailFlowSend uses a **stable native C ABI** inside the Wails host, while Go-heavy feature logic can execute in isolated worker processes.

## Why this design exists

The accepted architecture avoids loading multiple independent Go runtimes into the same Go/Wails process.

~~~text
Go/Wails host
→ stable C ABI
→ native DLL
→ isolated worker EXE when Go feature logic is required
~~~

This keeps the host runtime singular and gives worker crashes/timeouts a clearer process boundary.

## ABI baseline

`internal/moduleabi/contract.go` defines:

~~~text
ABI version      1
Core version     0.16.9
Max JSON bytes   1 MiB
execution_policy serialized | parallel
~~~

Manifest fields:

~~~text
id
name
version
abi
min_core
max_core
kind
file
capabilities[]
execution_policy
~~~

## Required exports

A native module loaded by ModuleHost must provide:

~~~text
MF_ABIVersion
MF_ModuleInfo
MF_Init
MF_Health
MF_Execute
MF_Shutdown
MF_Free
~~~

## Module discovery

ModuleHost scans the configured module root for `module.json`.

For each manifest it validates:

- manifest format;
- safe module-relative DLL path;
- ABI version;
- Core version compatibility;
- required exports;
- runtime identity returned by `MF_ModuleInfo`;
- declared capabilities;
- initialization;
- health.

DLL path traversal outside the manifest directory is rejected.

## Runtime identity

After loading, runtime `ModuleInfo` must match manifest:

~~~text
ID
Version
ABI
Capabilities
~~~

A mismatch fails the module rather than silently trusting one side.

## Native JSON memory ownership

JSON-returning exports return module-owned `char*`.

The host:

1. reads a bounded C string;
2. validates response size;
3. copies into Go memory;
4. calls module `MF_Free`.

The module must not expect the Go host to free native memory directly.

## Windows LastError rule

For ABI v1, return values are authoritative:

- `MF_ABIVersion`: returned scalar;
- `MF_Init`: `0` = success;
- JSON exports: non-NULL pointer = returned contract payload;
- NULL pointer = host-level failure.

Windows thread `GetLastError` can contain stale values after a successful native call, so it is diagnostic evidence only unless the ABI return value indicates failure.

## Execution policy

Default behavior is **serialized**.

A module gets parallel execution only if its manifest explicitly declares:

~~~json
"execution_policy": "parallel"
~~~

The execution gate separates:

- module lifecycle lock — protects load/refresh/unload;
- serialized execution lock — only for serialized modules.

This prevents DLL unload while `MF_Execute` is in flight.

## mail.smtp

Current manifest:

~~~text
id       mail.smtp
version  0.5.0
abi      1
kind     native_dll
policy   parallel
file     mail.smtp.dll
~~~

Capabilities:

~~~text
mail.transport.smtp
smtp.contract.describe
smtp.profile.validate
smtp.message.validate
smtp.message.compose
smtp.send
smtp.test_connection
smtp.protocol_trace
~~~

### SMTP worker architecture

~~~mermaid
sequenceDiagram
    participant H as Go Host
    participant D as mail.smtp.dll
    participant W as mail.smtp.worker.exe
    participant S as SMTP server

    H->>D: MF_Execute(request JSON)
    D->>D: write bounded temp request
    D->>W: CreateProcessW
    W->>W: resolve Windows credential
    W->>S: SMTP/TLS/AUTH/send
    S-->>W: protocol result
    W->>D: bounded response file
    D-->>H: response JSON
~~~

The DLL itself does not implement SMTP protocol logic. It launches the worker beside the DLL.

Safety bounds visible in native bridge:

~~~text
request JSON max      256 KiB
response max          900 KiB
worker timeout        130 seconds
~~~

Temporary request/response files are deleted after execution.

The worker supports an out-of-band cancellation marker used by the concurrency contract.

## mail.debt

Current manifest:

~~~text
id       mail.debt
version  0.3.1
abi      1
kind     native_dll
file     mail.debt.dll
policy   default serialized
~~~

Capabilities:

~~~text
debt.import.preview
debt.import.parse
debt.normalize
debt.validate
~~~

The native bridge launches `mail.debt.worker.exe`, which imports `internal/debtparser`.

Current native bounds:

~~~text
request JSON max      128 KiB
response max          900 KiB
worker timeout        60 seconds
~~~

## Why workers use temp files

The DLL ABI stays small and stable while worker request/response data can be exchanged as bounded UTF-8 JSON.

This also avoids putting raw Go object pointers or Go runtime memory across the C ABI.

## Adding a module

Recommended contract:

1. create a manifest;
2. use ABI 1 unless a deliberate ABI migration is approved;
3. default to serialized execution;
4. opt into parallel only after concurrency tests;
5. implement all required exports;
6. keep JSON responses bounded;
7. validate runtime identity;
8. add adversarial native-memory tests;
9. add Windows runtime acceptance;
10. expose health through ModuleHost/Diagnostics.

## Do not

- load arbitrary DLL paths outside module root;
- silently accept ABI mismatch;
- free module memory from Go without `MF_Free`;
- treat stale LastError as failure when ABI return succeeded;
- enable parallel execution merely for performance;
- embed a second Go runtime into the Wails process without an accepted safety design.
