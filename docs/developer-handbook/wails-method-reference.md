# Wails Method Semantic Reference

This page catalogs the complete generated Wails binding surface for the documented source baseline.

~~~text
Source SHA 0aae214a2e6324b09b4ad1b093fae174abc5ebb0
Binding    frontend/wailsjs/go/main/App.d.ts
Methods    242
~~~

## How to read this reference

- **Exact signature** is copied from the generated TypeScript binding.
- **Domain** groups methods by their owning product area.
- **Operation class** describes the interface behavior: read, preview/advisory, mutation, external I/O, file export, desktop navigation, etc.
- **Semantic** is a concise normalized description from the exported API name. For safety-critical business rules, follow the linked domain handbook/runbook and the Go implementation; this catalog does not override Core validation.

Frontend code should call these bindings asynchronously and must not reproduce Core business rules locally.

## Operation classes

| Class | Meaning |
|---|---|
| Read | query current durable/read-model state |
| Preview / advisory | calculate or validate without committing the final business action |
| Mutation | change durable domain/configuration state |
| Controlled operation | explicit bounded operation that can create evidence/state |
| External test/send/scan | network or external side effect boundary |
| Desktop picker/navigation | native file/folder/UI integration |
| File export | writes an operator-requested export |
| Module execution | invokes runtime module capability |

## Core / Runtime

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ExecuteModule | Module execution | Execute Module | export function ExecuteModule(arg1:string,arg2:string):Promise&lt;main.ExecuteResult&gt;; |
| GetCoreStatus | Read | Read current/detail Core Status | export function GetCoreStatus():Promise&lt;coredb.Status&gt;; |
| GetModuleSnapshot | Read | Read current/detail Module Snapshot | export function GetModuleSnapshot():Promise&lt;modulehost.Snapshot&gt;; |
| GetRuntimeSafety | Read | Read current/detail Runtime Safety | export function GetRuntimeSafety():Promise&lt;main.RuntimeSafetyView&gt;; |
| OpenCoreDatabaseFolder | Desktop navigation | Open desktop location for Core Database Folder | export function OpenCoreDatabaseFolder():Promise&lt;void&gt;; |
| RefreshCoreStatus | Refresh | Refresh Core Status | export function RefreshCoreStatus():Promise&lt;coredb.Status&gt;; |
| RefreshModules | Refresh | Refresh Modules | export function RefreshModules():Promise&lt;modulehost.Snapshot&gt;; |

## Clients / CSM

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddClientContact | Mutation | Add Client Contact | export function AddClientContact(arg1:number,arg2:string,arg3:boolean,arg4:string):Promise&lt;coredb.ClientContactMutationResult&gt;; |
| DeactivateClientContact | Mutation | Deactivate Client Contact | export function DeactivateClientContact(arg1:number,arg2:string):Promise&lt;coredb.ClientContactMutationResult&gt;; |
| GetClient | Read | Read current/detail Client | export function GetClient(arg1:number):Promise&lt;coredb.ClientDetail&gt;; |
| GetClientRegistryQualityDetails | Read | Read current/detail Client Registry Quality Details | export function GetClientRegistryQualityDetails(arg1:number):Promise&lt;coredb.ClientRegistryQualityDetails&gt;; |
| ListCSMs | Read | List CS Ms | export function ListCSMs():Promise&lt;Array&lt;coredb.CSMView&gt;&gt;; |
| ListClientCSMTransferEvents | Read | List Client CSM Transfer Events | export function ListClientCSMTransferEvents(arg1:number):Promise&lt;Array&lt;coredb.ClientCSMTransferEventView&gt;&gt;; |
| ListClientContactEvents | Read | List Client Contact Events | export function ListClientContactEvents(arg1:number):Promise&lt;Array&lt;coredb.ClientContactEventView&gt;&gt;; |
| ListClientCooperationStatusEvents | Read | List Client Cooperation Status Events | export function ListClientCooperationStatusEvents(arg1:number):Promise&lt;Array&lt;coredb.ClientCooperationStatusEventView&gt;&gt;; |
| ListClientRegistry | Read | List Client Registry | export function ListClientRegistry(arg1:string,arg2:number,arg3:number,arg4:number):Promise&lt;coredb.ClientRegistryPage&gt;; |
| ListClientRegistryFiltered | Read | List Client Registry Filtered | export function ListClientRegistryFiltered(arg1:string,arg2:number,arg3:string,arg4:number,arg5:number):Promise&lt;coredb.ClientRegistryPage&gt;; |
| ListClientRegistryIntakeEvents | Read | List Client Registry Intake Events | export function ListClientRegistryIntakeEvents(arg1:number):Promise&lt;Array&lt;coredb.ClientRegistryIntakeEventView&gt;&gt;; |
| ListClientRegistryQuality | Read | List Client Registry Quality | export function ListClientRegistryQuality(arg1:string,arg2:number,arg3:string,arg4:string,arg5:number,arg6:number):Promise&lt;coredb.ClientRegistryQualityPage&gt;; |
| ListClients | Read | List Clients | export function ListClients(arg1:string,arg2:number):Promise&lt;Array&lt;coredb.ClientView&gt;&gt;; |
| PreviewClientCSMTransfer | Preview / advisory | Preview/validate without commit Client CSM Transfer | export function PreviewClientCSMTransfer(arg1:number,arg2:number):Promise&lt;coredb.ClientCSMTransferPreview&gt;; |
| PreviewClientCooperationStatusChange | Preview / advisory | Preview/validate without commit Client Cooperation Status Change | export function PreviewClientCooperationStatusChange(arg1:number,arg2:string):Promise&lt;coredb.ClientCooperationStatusPreview&gt;; |
| ReactivateClientContact | Mutation | Reactivate Client Contact | export function ReactivateClientContact(arg1:number,arg2:boolean,arg3:string):Promise&lt;coredb.ClientContactMutationResult&gt;; |
| SetClientCooperationStatus | Mutation | Set Client Cooperation Status | export function SetClientCooperationStatus(arg1:number,arg2:string,arg3:string):Promise&lt;coredb.ClientCooperationStatusResult&gt;; |
| SetPrimaryClientContact | Mutation | Set Primary Client Contact | export function SetPrimaryClientContact(arg1:number,arg2:string):Promise&lt;coredb.ClientContactMutationResult&gt;; |
| TransferClientCSM | Mutation | Transfer Client CSM | export function TransferClientCSM(arg1:number,arg2:number,arg3:string):Promise&lt;coredb.ClientCSMTransferResult&gt;; |
| UpdateClientContact | Mutation | Update Client Contact | export function UpdateClientContact(arg1:number,arg2:string,arg3:boolean,arg4:string):Promise&lt;coredb.ClientContactMutationResult&gt;; |

## Attachments / Reconciliation

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ChooseAttachmentBatchFolder | Desktop picker | Open desktop picker for Attachment Batch Folder | export function ChooseAttachmentBatchFolder():Promise&lt;string&gt;; |
| ClassifyAttachmentOrphans | Mutation | Classify Classify Attachment Orphans | export function ClassifyAttachmentOrphans(arg1:number):Promise&lt;coredb.OrphanClassificationSummary&gt;; |
| CreateCampaignPreflightAttachmentResolution | Mutation | Create Campaign Preflight Attachment Resolution | export function CreateCampaignPreflightAttachmentResolution(arg1:number):Promise&lt;coredb.CampaignPreflightAttachmentResolutionView&gt;; |
| CreateClientFromMissingOrphan | Mutation | Create Client From Missing Orphan | export function CreateClientFromMissingOrphan(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:string,arg7:string,arg8:string,arg9:boolean):Promise&lt;coredb.ClientRegistryIntakeResult&gt;; |
| DeferMissingClientVerification | Mutation | Defer Defer Missing Client Verification | export function DeferMissingClientVerification(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string):Promise&lt;coredb.ReconciliationResult&gt;; |
| DismissReconciliationCase | Mutation | Dismiss Dismiss Reconciliation Case | export function DismissReconciliationCase(arg1:number,arg2:string):Promise&lt;coredb.ReconciliationResult&gt;; |
| GetAttachmentMatchSummary | Read | Read current/detail Attachment Match Summary | export function GetAttachmentMatchSummary(arg1:number):Promise&lt;coredb.AttachmentMatchSummary&gt;; |
| GetCampaignPreflightAttachmentResolution | Read | Read current/detail Campaign Preflight Attachment Resolution | export function GetCampaignPreflightAttachmentResolution(arg1:number):Promise&lt;coredb.CampaignPreflightAttachmentResolutionView&gt;; |
| GetOrphanClassificationSummary | Read | Read current/detail Orphan Classification Summary | export function GetOrphanClassificationSummary(arg1:number):Promise&lt;coredb.OrphanClassificationSummary&gt;; |
| GetReconciliationSummary | Read | Read current/detail Reconciliation Summary | export function GetReconciliationSummary(arg1:number):Promise&lt;coredb.ReconciliationSummary&gt;; |
| IndexAttachmentBatch | Mutation | Index Attachment Batch | export function IndexAttachmentBatch(arg1:string):Promise&lt;coredb.AttachmentBatchView&gt;; |
| ListAttachmentBatches | Read | List Attachment Batches | export function ListAttachmentBatches():Promise&lt;Array&lt;coredb.AttachmentBatchView&gt;&gt;; |
| ListAttachmentMatchResults | Read | List Attachment Match Results | export function ListAttachmentMatchResults(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.AttachmentMatchView&gt;&gt;; |
| ListAttachmentPeriodCounts | Read | List Attachment Period Counts | export function ListAttachmentPeriodCounts(arg1:number):Promise&lt;Array&lt;coredb.PeriodCount&gt;&gt;; |
| ListAttachmentResolutionEvents | Read | List Attachment Resolution Events | export function ListAttachmentResolutionEvents(arg1:number):Promise&lt;Array&lt;coredb.AttachmentResolutionEventView&gt;&gt;; |
| ListAttachments | Read | List Attachments | export function ListAttachments(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.AttachmentView&gt;&gt;; |
| ListCampaignPreflightAttachmentResolutions | Read | List Campaign Preflight Attachment Resolutions | export function ListCampaignPreflightAttachmentResolutions(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.CampaignPreflightAttachmentResolutionView&gt;&gt;; |
| ListClientAttachmentBatchStates | Read | List Client Attachment Batch States | export function ListClientAttachmentBatchStates(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.ClientAttachmentBatchStateView&gt;&gt;; |
| ListOrphanClassifications | Read | List Orphan Classifications | export function ListOrphanClassifications(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.OrphanClassificationView&gt;&gt;; |
| ListReconciliationCases | Read | List Reconciliation Cases | export function ListReconciliationCases(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.ReconciliationCaseView&gt;&gt;; |
| ListUnavailableAttachmentIssues | Read | List Unavailable Attachment Issues | export function ListUnavailableAttachmentIssues(arg1:number,arg2:number):Promise&lt;coredb.AttachmentAvailabilityIssuePage&gt;; |
| OpenUnavailableAttachmentFolder | Desktop navigation | Open desktop location for Unavailable Attachment Folder | export function OpenUnavailableAttachmentFolder(arg1:number):Promise&lt;void&gt;; |
| PreviewAliasLearning | Preview / advisory | Preview/validate without commit Alias Learning | export function PreviewAliasLearning(arg1:number,arg2:number,arg3:number,arg4:string):Promise&lt;coredb.AliasLearningPreview&gt;; |
| PreviewMissingClientIntake | Preview / advisory | Preview/validate without commit Missing Client Intake | export function PreviewMissingClientIntake(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:string,arg7:string):Promise&lt;coredb.ClientRegistryIntakePreview&gt;; |
| ProbeUnavailableAttachment | Mutation | Probe Probe Unavailable Attachment | export function ProbeUnavailableAttachment(arg1:number):Promise&lt;coredb.AttachmentAvailabilityProbe&gt;; |
| RemoveManualAttachmentResolution | Mutation | Remove Manual Attachment Resolution | export function RemoveManualAttachmentResolution(arg1:number,arg2:number,arg3:string):Promise&lt;coredb.OrphanResolutionResult&gt;; |
| ResolveOrphanManual | Mutation | Resolve Orphan Manual | export function ResolveOrphanManual(arg1:number,arg2:number,arg3:number,arg4:string):Promise&lt;coredb.OrphanResolutionResult&gt;; |
| ResolveOrphanWithAlias | Mutation | Resolve Orphan With Alias | export function ResolveOrphanWithAlias(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string):Promise&lt;coredb.OrphanResolutionResult&gt;; |
| RunAttachmentMatcher | Controlled operation | Run controlled Attachment Matcher | export function RunAttachmentMatcher(arg1:number):Promise&lt;coredb.AttachmentMatchSummary&gt;; |
| SearchExistingClientsForMissingOrphan | Preview / advisory | Search advisory candidates Existing Clients For Missing Orphan | export function SearchExistingClientsForMissingOrphan(arg1:number,arg2:number,arg3:string,arg4:number):Promise&lt;coredb.ExistingClientSearchResponse&gt;; |
| SetAttachmentExpectedPeriod | Mutation | Set Attachment Expected Period | export function SetAttachmentExpectedPeriod(arg1:number,arg2:string):Promise&lt;coredb.AttachmentBatchView&gt;; |
| SuggestAttachmentAlias | Preview / advisory | Suggest advisory value Attachment Alias | export function SuggestAttachmentAlias(arg1:string):Promise&lt;string&gt;; |
| UpdateReconciliationCase | Mutation | Update Reconciliation Case | export function UpdateReconciliationCase(arg1:number,arg2:number,arg3:string):Promise&lt;coredb.ReconciliationResult&gt;; |

## GENERAL

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddGeneralCampaignAttachments | Mutation | Add General Campaign Attachments | export function AddGeneralCampaignAttachments(arg1:number,arg2:Array&lt;string&gt;):Promise&lt;coredb.CampaignDetail&gt;; |
| AddMailingContact | Mutation | Add Mailing Contact | export function AddMailingContact(arg1:string,arg2:string,arg3:string,arg4:string):Promise&lt;coredb.MailingContactMutationResult&gt;; |
| AddMailingGroup | Mutation | Add Mailing Group | export function AddMailingGroup(arg1:string,arg2:string):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |
| AddMailingTag | Mutation | Add Mailing Tag | export function AddMailingTag(arg1:string,arg2:string):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |
| ChooseGeneralCampaignAttachments | Desktop picker | Open desktop picker for General Campaign Attachments | export function ChooseGeneralCampaignAttachments():Promise&lt;Array&lt;string&gt;&gt;; |
| ChooseMailingContactImportFile | Desktop picker | Open desktop picker for Mailing Contact Import File | export function ChooseMailingContactImportFile():Promise&lt;string&gt;; |
| CommitMailingContactImport | Mutation | Commit Mailing Contact Import | export function CommitMailingContactImport(arg1:string,arg2:string,arg3:coredb.MailingImportMapping,arg4:string,arg5:string,arg6:Array&lt;number&gt;,arg7:Array&lt;number&gt;):Promise&lt;coredb.MailingContactImportResult&gt;; |
| CreateGeneralCampaignDraft | Mutation | Create General Campaign Draft | export function CreateGeneralCampaignDraft(arg1:string,arg2:Array&lt;number&gt;,arg3:Array&lt;number&gt;,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string):Promise&lt;coredb.CampaignDetail&gt;; |
| InspectMailingContactImport | Preview / advisory | Inspect source Mailing Contact Import | export function InspectMailingContactImport(arg1:string,arg2:string):Promise&lt;coredb.MailingContactImportInspection&gt;; |
| ListMailingContactEvents | Read | List Mailing Contact Events | export function ListMailingContactEvents(arg1:number):Promise&lt;Array&lt;coredb.MailingContactEventView&gt;&gt;; |
| ListMailingContactImports | Read | List Mailing Contact Imports | export function ListMailingContactImports(arg1:number):Promise&lt;Array&lt;coredb.MailingContactImportHistoryView&gt;&gt;; |
| ListMailingContacts | Read | List Mailing Contacts | export function ListMailingContacts():Promise&lt;Array&lt;coredb.MailingContactView&gt;&gt;; |
| ListMailingGroups | Read | List Mailing Groups | export function ListMailingGroups():Promise&lt;Array&lt;coredb.MailingGroupView&gt;&gt;; |
| ListMailingTags | Read | List Mailing Tags | export function ListMailingTags():Promise&lt;Array&lt;coredb.MailingTagView&gt;&gt;; |
| ListMailingTaxonomyEvents | Read | List Mailing Taxonomy Events | export function ListMailingTaxonomyEvents(arg1:string,arg2:number):Promise&lt;Array&lt;coredb.MailingTaxonomyEventView&gt;&gt;; |
| PreviewGeneralCampaignRecipient | Preview / advisory | Preview/validate without commit General Campaign Recipient | export function PreviewGeneralCampaignRecipient(arg1:number,arg2:number):Promise&lt;coredb.GeneralCampaignRecipientPreview&gt;; |
| PreviewMailingContactImport | Preview / advisory | Preview/validate without commit Mailing Contact Import | export function PreviewMailingContactImport(arg1:string,arg2:string,arg3:coredb.MailingImportMapping,arg4:string,arg5:Array&lt;number&gt;,arg6:Array&lt;number&gt;):Promise&lt;coredb.MailingContactImportPreview&gt;; |
| RemoveGeneralCampaignAttachment | Mutation | Remove General Campaign Attachment | export function RemoveGeneralCampaignAttachment(arg1:number,arg2:number):Promise&lt;coredb.CampaignDetail&gt;; |
| SetGeneralCampaignAudienceAll | Mutation | Set General Campaign Audience All | export function SetGeneralCampaignAudienceAll(arg1:number,arg2:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| SetGeneralCampaignAudienceIncluded | Mutation | Set General Campaign Audience Included | export function SetGeneralCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| SetMailingContactGroup | Mutation | Set Mailing Contact Group | export function SetMailingContactGroup(arg1:number,arg2:number,arg3:boolean):Promise&lt;coredb.MailingMembershipMutationResult&gt;; |
| SetMailingContactStatus | Mutation | Set Mailing Contact Status | export function SetMailingContactStatus(arg1:number,arg2:string,arg3:string):Promise&lt;coredb.MailingContactMutationResult&gt;; |
| SetMailingContactTag | Mutation | Set Mailing Contact Tag | export function SetMailingContactTag(arg1:number,arg2:number,arg3:boolean):Promise&lt;coredb.MailingMembershipMutationResult&gt;; |
| SetMailingContactsGroup | Mutation | Set Mailing Contacts Group | export function SetMailingContactsGroup(arg1:Array&lt;number&gt;,arg2:number,arg3:boolean):Promise&lt;coredb.MailingBulkMembershipResult&gt;; |
| SetMailingContactsTag | Mutation | Set Mailing Contacts Tag | export function SetMailingContactsTag(arg1:Array&lt;number&gt;,arg2:number,arg3:boolean):Promise&lt;coredb.MailingBulkMembershipResult&gt;; |
| SetMailingGroupActive | Mutation | Set Mailing Group Active | export function SetMailingGroupActive(arg1:number,arg2:boolean):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |
| SetMailingTagActive | Mutation | Set Mailing Tag Active | export function SetMailingTagActive(arg1:number,arg2:boolean):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |
| UpdateGeneralCampaignDraft | Mutation | Update General Campaign Draft | export function UpdateGeneralCampaignDraft(arg1:number,arg2:string,arg3:Array&lt;number&gt;,arg4:Array&lt;number&gt;,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string):Promise&lt;coredb.CampaignDetail&gt;; |
| UpdateMailingContact | Mutation | Update Mailing Contact | export function UpdateMailingContact(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string):Promise&lt;coredb.MailingContactMutationResult&gt;; |
| UpdateMailingGroup | Mutation | Update Mailing Group | export function UpdateMailingGroup(arg1:number,arg2:string,arg3:string):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |
| UpdateMailingTag | Mutation | Update Mailing Tag | export function UpdateMailingTag(arg1:number,arg2:string,arg3:string):Promise&lt;coredb.MailingTaxonomyMutationResult&gt;; |

## DEBT

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddDebtCampaignAttachments | Mutation | Add Debt Campaign Attachments | export function AddDebtCampaignAttachments(arg1:number,arg2:Array&lt;string&gt;):Promise&lt;coredb.CampaignDetail&gt;; |
| ChooseDebtCampaignAttachments | Desktop picker | Open desktop picker for Debt Campaign Attachments | export function ChooseDebtCampaignAttachments():Promise&lt;Array&lt;string&gt;&gt;; |
| ChooseDebtImportFile | Desktop picker | Open desktop picker for Debt Import File | export function ChooseDebtImportFile():Promise&lt;string&gt;; |
| CreateDebtImportSnapshot | Mutation | Create Debt Import Snapshot | export function CreateDebtImportSnapshot(arg1:string,arg2:string,arg3:number,arg4:Record&lt;string, number&gt;):Promise&lt;coredb.DebtImportSnapshotResult&gt;; |
| CreateDebtNoticeCampaignDraft | Mutation | Create Debt Notice Campaign Draft | export function CreateDebtNoticeCampaignDraft(arg1:string,arg2:number,arg3:string,arg4:string,arg5:string,arg6:string):Promise&lt;coredb.CampaignDetail&gt;; |
| GetDebtImportSnapshot | Read | Read current/detail Debt Import Snapshot | export function GetDebtImportSnapshot(arg1:number):Promise&lt;coredb.DebtImportSnapshotResult&gt;; |
| ListDebtImports | Read | List Debt Imports | export function ListDebtImports(arg1:number):Promise&lt;Array&lt;coredb.DebtImportView&gt;&gt;; |
| ListDebtReconciliationCases | Read | List Debt Reconciliation Cases | export function ListDebtReconciliationCases(arg1:string):Promise&lt;Array&lt;coredb.DebtReconciliationCaseView&gt;&gt;; |
| PreviewDebtCampaignRecipient | Preview / advisory | Preview/validate without commit Debt Campaign Recipient | export function PreviewDebtCampaignRecipient(arg1:number,arg2:number):Promise&lt;coredb.DebtCampaignRecipientPreview&gt;; |
| PreviewDebtCampaignRecipientIdentity | Preview / advisory | Preview/validate without commit Debt Campaign Recipient Identity | export function PreviewDebtCampaignRecipientIdentity(arg1:number,arg2:number,arg3:string):Promise&lt;coredb.DebtCampaignRecipientPreview&gt;; |
| RemoveDebtCampaignAttachment | Mutation | Remove Debt Campaign Attachment | export function RemoveDebtCampaignAttachment(arg1:number,arg2:number):Promise&lt;coredb.CampaignDetail&gt;; |
| ResolveDebtReconciliationCase | Mutation | Resolve Debt Reconciliation Case | export function ResolveDebtReconciliationCase(arg1:number,arg2:number,arg3:string):Promise&lt;coredb.DebtReconciliationResult&gt;; |
| RunDebtClientMatching | Controlled operation | Run controlled Debt Client Matching | export function RunDebtClientMatching(arg1:string,arg2:string,arg3:number,arg4:Record&lt;string, number&gt;):Promise&lt;coredb.DebtMatchingResult&gt;; |
| SearchDebtClientCandidates | Preview / advisory | Search advisory candidates Debt Client Candidates | export function SearchDebtClientCandidates(arg1:string,arg2:number):Promise&lt;Array&lt;coredb.DebtClientCandidate&gt;&gt;; |
| SetDebtCampaignAudienceAll | Mutation | Set Debt Campaign Audience All | export function SetDebtCampaignAudienceAll(arg1:number,arg2:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| SetDebtCampaignAudienceIncluded | Mutation | Set Debt Campaign Audience Included | export function SetDebtCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| UpdateDebtNoticeCampaignDraft | Mutation | Update Debt Notice Campaign Draft | export function UpdateDebtNoticeCampaignDraft(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string):Promise&lt;coredb.CampaignDetail&gt;; |

## Campaign / Preflight

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddSenderProfile | Mutation | Add Sender Profile | export function AddSenderProfile(arg1:string,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string,arg7:string):Promise&lt;coredb.SenderProfileMutationResult&gt;; |
| CreateCampaignDispatchSnapshot | Mutation | Create Campaign Dispatch Snapshot | export function CreateCampaignDispatchSnapshot(arg1:number):Promise&lt;coredb.CampaignDispatchSnapshotView&gt;; |
| CreateCampaignDraft | Mutation | Create Campaign Draft | export function CreateCampaignDraft(arg1:string,arg2:number,arg3:string,arg4:Array&lt;number&gt;,arg5:string,arg6:string,arg7:string):Promise&lt;coredb.CampaignDetail&gt;; |
| CreateCampaignPreflightEligibility | Mutation | Create Campaign Preflight Eligibility | export function CreateCampaignPreflightEligibility(arg1:number):Promise&lt;coredb.CampaignPreflightEligibilityView&gt;; |
| CreateCampaignPreflightFoundation | Mutation | Create Campaign Preflight Foundation | export function CreateCampaignPreflightFoundation(arg1:number):Promise&lt;coredb.CampaignPreflightFoundationView&gt;; |
| CreateCampaignPreflightRecipientResolution | Mutation | Create Campaign Preflight Recipient Resolution | export function CreateCampaignPreflightRecipientResolution(arg1:number):Promise&lt;coredb.CampaignPreflightRecipientResolutionView&gt;; |
| CreateDocumentsCatchUpCampaign | Mutation | Create Documents Catch Up Campaign | export function CreateDocumentsCatchUpCampaign(arg1:number):Promise&lt;coredb.DocumentsCatchUpCreateResult&gt;; |
| CreateManagedBackupLifecyclePreflight | Mutation | Create Managed Backup Lifecycle Preflight | export function CreateManagedBackupLifecyclePreflight(arg1:string,arg2:string):Promise&lt;recovery.BackupLifecyclePreflight&gt;; |
| ExcludeCampaignEligibilityBlocked | Mutation | Exclude Campaign Eligibility Blocked | export function ExcludeCampaignEligibilityBlocked(arg1:number,arg2:number):Promise&lt;coredb.CampaignEligibilityBlockedExclusionResult&gt;; |
| GetCampaign | Read | Read current/detail Campaign | export function GetCampaign(arg1:number):Promise&lt;coredb.CampaignDetail&gt;; |
| GetCampaignDispatchHandoff | Read | Read current/detail Campaign Dispatch Handoff | export function GetCampaignDispatchHandoff(arg1:number):Promise&lt;coredb.CampaignDispatchHandoffView&gt;; |
| GetCampaignDispatchSnapshot | Read | Read current/detail Campaign Dispatch Snapshot | export function GetCampaignDispatchSnapshot(arg1:number):Promise&lt;coredb.CampaignDispatchSnapshotView&gt;; |
| GetCampaignPreflightEligibility | Read | Read current/detail Campaign Preflight Eligibility | export function GetCampaignPreflightEligibility(arg1:number):Promise&lt;coredb.CampaignPreflightEligibilityView&gt;; |
| GetCampaignPreflightFoundation | Read | Read current/detail Campaign Preflight Foundation | export function GetCampaignPreflightFoundation(arg1:number):Promise&lt;coredb.CampaignPreflightFoundationView&gt;; |
| GetCampaignPreflightRecipientResolution | Read | Read current/detail Campaign Preflight Recipient Resolution | export function GetCampaignPreflightRecipientResolution(arg1:number):Promise&lt;coredb.CampaignPreflightRecipientResolutionView&gt;; |
| GetTemplateEngineStatus | Read | Read current/detail Template Engine Status | export function GetTemplateEngineStatus():Promise&lt;coredb.TemplateEngineStatusView&gt;; |
| ListCampaignDispatchSnapshots | Read | List Campaign Dispatch Snapshots | export function ListCampaignDispatchSnapshots(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.CampaignDispatchSnapshotView&gt;&gt;; |
| ListCampaignEvents | Read | List Campaign Events | export function ListCampaignEvents(arg1:number):Promise&lt;Array&lt;coredb.CampaignEventView&gt;&gt;; |
| ListCampaignPreflightEligibilities | Read | List Campaign Preflight Eligibilities | export function ListCampaignPreflightEligibilities(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.CampaignPreflightEligibilityView&gt;&gt;; |
| ListCampaignPreflightFoundations | Read | List Campaign Preflight Foundations | export function ListCampaignPreflightFoundations(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.CampaignPreflightFoundationView&gt;&gt;; |
| ListCampaignPreflightRecipientResolutions | Read | List Campaign Preflight Recipient Resolutions | export function ListCampaignPreflightRecipientResolutions(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.CampaignPreflightRecipientResolutionView&gt;&gt;; |
| ListCampaignTemplatePreviewRecipients | Read | List Campaign Template Preview Recipients | export function ListCampaignTemplatePreviewRecipients(arg1:number):Promise&lt;Array&lt;coredb.CampaignTemplatePreviewRecipientView&gt;&gt;; |
| ListCampaigns | Read | List Campaigns | export function ListCampaigns():Promise&lt;Array&lt;coredb.CampaignSummary&gt;&gt;; |
| ListSenderProfileEvents | Read | List Sender Profile Events | export function ListSenderProfileEvents(arg1:number):Promise&lt;Array&lt;coredb.SenderProfileEventView&gt;&gt;; |
| ListSenderProfiles | Read | List Sender Profiles | export function ListSenderProfiles():Promise&lt;Array&lt;coredb.SenderProfileView&gt;&gt;; |
| PreflightLegacyProject | Mutation | Preflight Preflight Legacy Project | export function PreflightLegacyProject(arg1:string):Promise&lt;legacyimport.FullImportPreflight&gt;; |
| PreviewCampaignTemplateRecipient | Preview / advisory | Preview/validate without commit Campaign Template Recipient | export function PreviewCampaignTemplateRecipient(arg1:coredb.CampaignTemplatePreviewRequest):Promise&lt;coredb.CampaignTemplatePreviewView&gt;; |
| SendDispatchRecipientToMailpit | External send | Send Dispatch Recipient To Mailpit | export function SendDispatchRecipientToMailpit(arg1:number,arg2:number,arg3:number):Promise&lt;mailtransport.Response&gt;; |
| SetCampaignAudienceAll | Mutation | Set Campaign Audience All | export function SetCampaignAudienceAll(arg1:number,arg2:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| SetCampaignAudienceIncluded | Mutation | Set Campaign Audience Included | export function SetCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise&lt;coredb.CampaignDetail&gt;; |
| SetSenderProfileActive | Mutation | Set Sender Profile Active | export function SetSenderProfileActive(arg1:number,arg2:boolean,arg3:string):Promise&lt;coredb.SenderProfileMutationResult&gt;; |
| SetTemplateEngineSpintaxEnabled | Mutation | Set Template Engine Spintax Enabled | export function SetTemplateEngineSpintaxEnabled(arg1:boolean):Promise&lt;coredb.TemplateEngineStatusView&gt;; |
| UpdateCampaignDraft | Mutation | Update Campaign Draft | export function UpdateCampaignDraft(arg1:number,arg2:string,arg3:number,arg4:string,arg5:Array&lt;number&gt;,arg6:string,arg7:string,arg8:string):Promise&lt;coredb.CampaignDetail&gt;; |
| UpdateSenderProfile | Mutation | Update Sender Profile | export function UpdateSenderProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string,arg7:string,arg8:string):Promise&lt;coredb.SenderProfileMutationResult&gt;; |

## SMTP

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddSMTPProfile | Mutation | Add SMTP Profile | export function AddSMTPProfile(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:number):Promise&lt;coredb.SMTPProfileMutationResult&gt;; |
| AddSMTPProfileV2 | Mutation | Add SMTP Profile V2 | export function AddSMTPProfileV2(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:number):Promise&lt;coredb.SMTPProfileMutationResult&gt;; |
| DeleteSMTPProfileCredential | Mutation | Delete SMTP Profile Credential | export function DeleteSMTPProfileCredential(arg1:number):Promise&lt;smtpcredential.MutationResult&gt;; |
| GetSMTPProfileCredentialStatus | Read | Read current/detail SMTP Profile Credential Status | export function GetSMTPProfileCredentialStatus(arg1:number):Promise&lt;smtpcredential.Status&gt;; |
| GetSMTPSessionDetail | Read | Read current/detail SMTP Session Detail | export function GetSMTPSessionDetail(arg1:number):Promise&lt;coredb.SMTPSessionDetail&gt;; |
| ListSMTPProfileEvents | Read | List SMTP Profile Events | export function ListSMTPProfileEvents(arg1:number):Promise&lt;Array&lt;coredb.SMTPProfileEventView&gt;&gt;; |
| ListSMTPProfiles | Read | List SMTP Profiles | export function ListSMTPProfiles():Promise&lt;Array&lt;coredb.SMTPProfileView&gt;&gt;; |
| ListSMTPSessions | Read | List SMTP Sessions | export function ListSMTPSessions(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.SMTPSessionView&gt;&gt;; |
| SendDispatchRecipientSMTP | External send | Send Dispatch Recipient SMTP | export function SendDispatchRecipientSMTP(arg1:number,arg2:number,arg3:number,arg4:boolean):Promise&lt;mailtransport.Response&gt;; |
| SetSMTPProfileActive | Mutation | Set SMTP Profile Active | export function SetSMTPProfileActive(arg1:number,arg2:boolean,arg3:string):Promise&lt;coredb.SMTPProfileMutationResult&gt;; |
| SetSMTPProfileCredential | Mutation | Set SMTP Profile Credential | export function SetSMTPProfileCredential(arg1:number,arg2:string):Promise&lt;smtpcredential.MutationResult&gt;; |
| TestSMTPProfileConnection | External test | Test SMTP Profile Connection | export function TestSMTPProfileConnection(arg1:number):Promise&lt;mailtransport.Response&gt;; |
| UpdateSMTPProfile | Mutation | Update SMTP Profile | export function UpdateSMTPProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:number):Promise&lt;coredb.SMTPProfileMutationResult&gt;; |
| UpdateSMTPProfileV2 | Mutation | Update SMTP Profile V2 | export function UpdateSMTPProfileV2(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:string,arg13:number):Promise&lt;coredb.SMTPProfileMutationResult&gt;; |

## Queue / Attempt

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| CancelSendQueue | Mutation | Cancel Send Queue | export function CancelSendQueue(arg1:number):Promise&lt;coredb.SendQueueJobView&gt;; |
| CreateSendQueue | Mutation | Create Send Queue | export function CreateSendQueue(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number):Promise&lt;coredb.SendQueueDetail&gt;; |
| GetDeliveryUnknownReviewDetail | Read | Read current/detail Delivery Unknown Review Detail | export function GetDeliveryUnknownReviewDetail(arg1:number):Promise&lt;coredb.DeliveryUnknownReviewDetail&gt;; |
| GetSendQueueDetail | Read | Read current/detail Send Queue Detail | export function GetSendQueueDetail(arg1:number):Promise&lt;coredb.SendQueueDetail&gt;; |
| ListDeliveryUnknownReviews | Read | List Delivery Unknown Reviews | export function ListDeliveryUnknownReviews(arg1:number,arg2:string):Promise&lt;Array&lt;coredb.DeliveryUnknownReviewView&gt;&gt;; |
| ListSendAttempts | Read | List Send Attempts | export function ListSendAttempts(arg1:number):Promise&lt;Array&lt;coredb.SendAttemptView&gt;&gt;; |
| ListSendQueues | Read | List Send Queues | export function ListSendQueues(arg1:number):Promise&lt;Array&lt;coredb.SendQueueJobView&gt;&gt;; |
| PauseSendQueue | Mutation | Pause Send Queue | export function PauseSendQueue(arg1:number):Promise&lt;coredb.SendQueueJobView&gt;; |
| ResolveDeliveryUnknownReview | Mutation | Resolve Delivery Unknown Review | export function ResolveDeliveryUnknownReview(arg1:number,arg2:string,arg3:string):Promise&lt;coredb.DeliveryUnknownReviewDetail&gt;; |
| ResumeSendQueue | Mutation | Resume Send Queue | export function ResumeSendQueue(arg1:number):Promise&lt;coredb.SendQueueJobView&gt;; |
| RetrySendQueueItemNow | Mutation | Retry Send Queue Item Now | export function RetrySendQueueItemNow(arg1:number):Promise&lt;coredb.SendQueueItemView&gt;; |
| StartSendQueue | Mutation | Start Send Queue | export function StartSendQueue(arg1:number,arg2:boolean):Promise&lt;coredb.SendQueueJobView&gt;; |

## Delivery / History

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ExportDeliveryHistory | File export | Export Delivery History | export function ExportDeliveryHistory(arg1:coredb.DeliveryHistoryWorkspaceQuery,arg2:string):Promise&lt;string&gt;; |
| ExportDeliveryHistoryConfigured | File export | Export Delivery History Configured | export function ExportDeliveryHistoryConfigured(arg1:coredb.DeliveryHistoryWorkspaceQuery,arg2:string,arg3:Array&lt;string&gt;):Promise&lt;string&gt;; |
| GetBounceDeliveryIntelligence | Read | Read current/detail Bounce Delivery Intelligence | export function GetBounceDeliveryIntelligence(arg1:number,arg2:string):Promise&lt;coredb.BounceDeliveryIntelligenceSnapshot&gt;; |
| GetClientMonthActivity | Read | Read current/detail Client Month Activity | export function GetClientMonthActivity(arg1:string,arg2:string):Promise&lt;coredb.ClientMonthActivityProjection&gt;; |
| GetClientMonthEvidence | Read | Read current/detail Client Month Evidence | export function GetClientMonthEvidence(arg1:number,arg2:string):Promise&lt;coredb.ClientMonthEvidenceView&gt;; |
| GetClientMonthSignals | Read | Read current/detail Client Month Signals | export function GetClientMonthSignals(arg1:string,arg2:string):Promise&lt;coredb.ClientMonthSignalProjection&gt;; |
| GetDeliveryHistoryDetail | Read | Read current/detail Delivery History Detail | export function GetDeliveryHistoryDetail(arg1:number):Promise&lt;coredb.DeliveryHistoryDetail&gt;; |
| GetDeliveryHistorySummary | Read | Read current/detail Delivery History Summary | export function GetDeliveryHistorySummary():Promise&lt;coredb.DeliveryHistorySummary&gt;; |
| GetDocumentsMonthlyCoverage | Read | Read current/detail Documents Monthly Coverage | export function GetDocumentsMonthlyCoverage(arg1:number):Promise&lt;coredb.DocumentsMonthlyCoverageView&gt;; |
| ListBouncedRecipientReviews | Read | List Bounced Recipient Reviews | export function ListBouncedRecipientReviews(arg1:number):Promise&lt;Array&lt;coredb.BouncedRecipientReviewView&gt;&gt;; |
| ListDeliveryHistory | Read | List Delivery History | export function ListDeliveryHistory(arg1:number,arg2:string,arg3:number):Promise&lt;Array&lt;coredb.DeliveryRecordView&gt;&gt;; |
| PrepareBouncedRecipientResend | Mutation | Prepare Prepare Bounced Recipient Resend | export function PrepareBouncedRecipientResend(arg1:number):Promise&lt;coredb.BounceResendCreateResult&gt;; |
| QueryDeliveryHistoryWorkspace | Read | Query Delivery History Workspace | export function QueryDeliveryHistoryWorkspace(arg1:coredb.DeliveryHistoryWorkspaceQuery):Promise&lt;coredb.DeliveryHistoryWorkspacePage&gt;; |

## DSN

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ChooseDSNArtifactFile | Desktop picker | Open desktop picker for DSN Artifact File | export function ChooseDSNArtifactFile():Promise&lt;string&gt;; |
| ConfirmDSNManualReconciliation | Mutation | Confirm DSN Manual Reconciliation | export function ConfirmDSNManualReconciliation(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:boolean):Promise&lt;coredb.DSNManualReconciliationResult&gt;; |
| GetDSNArtifactDetail | Read | Read current/detail DSN Artifact Detail | export function GetDSNArtifactDetail(arg1:number):Promise&lt;coredb.DSNArtifactDetail&gt;; |
| GetDSNMessageIDDiagnostics | Read | Read current/detail DSN Message ID Diagnostics | export function GetDSNMessageIDDiagnostics(arg1:number):Promise&lt;coredb.DSNMessageIDDiagnosticsView&gt;; |
| IngestDSNArtifactFile | Mutation | Ingest Ingest DSN Artifact File | export function IngestDSNArtifactFile(arg1:string):Promise&lt;coredb.DSNIngestionResult&gt;; |
| ListDSNArtifacts | Read | List DSN Artifacts | export function ListDSNArtifacts(arg1:string,arg2:number):Promise&lt;Array&lt;coredb.DSNArtifactView&gt;&gt;; |
| PreviewDSNManualReconciliation | Preview / advisory | Preview/validate without commit DSN Manual Reconciliation | export function PreviewDSNManualReconciliation(arg1:number,arg2:number,arg3:number):Promise&lt;coredb.DSNManualReconciliationPreview&gt;; |
| ReconcileDSNDeliveryProjection | Mutation | Reconcile DSN Delivery Projection | export function ReconcileDSNDeliveryProjection():Promise&lt;coredb.DSNDeliveryProjectionResult&gt;; |

## Inbound

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| AddInboundMailboxProfile | Mutation | Add Inbound Mailbox Profile | export function AddInboundMailboxProfile(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string):Promise&lt;inboundmailbox.ProfileMutationResult&gt;; |
| DeleteInboundMailboxCredential | Mutation | Delete Inbound Mailbox Credential | export function DeleteInboundMailboxCredential(arg1:number):Promise&lt;inboundmailbox.CredentialMutationResult&gt;; |
| GetInboundMailboxCredentialStatus | Read | Read current/detail Inbound Mailbox Credential Status | export function GetInboundMailboxCredentialStatus(arg1:number):Promise&lt;inboundmailbox.CredentialStatus&gt;; |
| GetInboundMailboxScanProgress | Read | Read current/detail Inbound Mailbox Scan Progress | export function GetInboundMailboxScanProgress(arg1:number):Promise&lt;inboundmailbox.ScanProgress&gt;; |
| GetInboundMailboxScanSchedule | Read | Read current/detail Inbound Mailbox Scan Schedule | export function GetInboundMailboxScanSchedule(arg1:number):Promise&lt;coredb.InboundMailboxScanScheduleView&gt;; |
| GetInboundMailboxScanState | Read | Read current/detail Inbound Mailbox Scan State | export function GetInboundMailboxScanState(arg1:number):Promise&lt;coredb.InboundMailboxScanStateView&gt;; |
| GetInboundMonitoringAlerts | Read | Read current/detail Inbound Monitoring Alerts | export function GetInboundMonitoringAlerts(arg1:number):Promise&lt;coredb.InboundMonitoringSnapshot&gt;; |
| ListInboundMailboxConnectionTests | Read | List Inbound Mailbox Connection Tests | export function ListInboundMailboxConnectionTests(arg1:number,arg2:number):Promise&lt;Array&lt;inboundmailbox.ConnectionTestResult&gt;&gt;; |
| ListInboundMailboxProfileEvents | Read | List Inbound Mailbox Profile Events | export function ListInboundMailboxProfileEvents(arg1:number):Promise&lt;Array&lt;inboundmailbox.ProfileEvent&gt;&gt;; |
| ListInboundMailboxProfiles | Read | List Inbound Mailbox Profiles | export function ListInboundMailboxProfiles():Promise&lt;Array&lt;inboundmailbox.InboundMailboxProfile&gt;&gt;; |
| ListInboundMailboxScanItems | Read | List Inbound Mailbox Scan Items | export function ListInboundMailboxScanItems(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.InboundMailboxScanItemView&gt;&gt;; |
| ListInboundMailboxScans | Read | List Inbound Mailbox Scans | export function ListInboundMailboxScans(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.InboundMailboxScanView&gt;&gt;; |
| ListInboundMailboxScheduleEvents | Read | List Inbound Mailbox Schedule Events | export function ListInboundMailboxScheduleEvents(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.InboundMailboxScheduleEventView&gt;&gt;; |
| ListInboundMailboxScheduleRuns | Read | List Inbound Mailbox Schedule Runs | export function ListInboundMailboxScheduleRuns(arg1:number,arg2:number):Promise&lt;Array&lt;coredb.InboundMailboxScheduleRunView&gt;&gt;; |
| ScanInboundMailbox | External scan | Scan Inbound Mailbox | export function ScanInboundMailbox(arg1:number,arg2:number):Promise&lt;coredb.InboundMailboxScanResult&gt;; |
| SetInboundMailboxCredential | Mutation | Set Inbound Mailbox Credential | export function SetInboundMailboxCredential(arg1:number,arg2:string):Promise&lt;inboundmailbox.CredentialMutationResult&gt;; |
| SetInboundMailboxProfileActive | Mutation | Set Inbound Mailbox Profile Active | export function SetInboundMailboxProfileActive(arg1:number,arg2:boolean,arg3:string):Promise&lt;inboundmailbox.ProfileMutationResult&gt;; |
| TestInboundMailboxConnection | External test | Test Inbound Mailbox Connection | export function TestInboundMailboxConnection(arg1:number):Promise&lt;inboundmailbox.ConnectionTestResult&gt;; |
| UpdateInboundMailboxProfile | Mutation | Update Inbound Mailbox Profile | export function UpdateInboundMailboxProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string):Promise&lt;inboundmailbox.ProfileMutationResult&gt;; |
| UpdateInboundMailboxScanSchedule | Mutation | Update Inbound Mailbox Scan Schedule | export function UpdateInboundMailboxScanSchedule(arg1:number,arg2:boolean,arg3:number,arg4:number):Promise&lt;coredb.InboundMailboxScanScheduleMutationResult&gt;; |

## Diagnostics / Logging

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| CaptureDiagnosticSnapshot | Evidence capture | Capture evidence for Diagnostic Snapshot | export function CaptureDiagnosticSnapshot():Promise&lt;main.DiagnosticHistoryCaptureResult&gt;; |
| ExportDiagnosticAIBundle | File export | Export Diagnostic AI Bundle | export function ExportDiagnosticAIBundle():Promise&lt;main.DiagnosticAIBundleExportResult&gt;; |
| GetCoreDiagnostics | Read | Read current/detail Core Diagnostics | export function GetCoreDiagnostics():Promise&lt;main.CoreDiagnostics&gt;; |
| GetDiagnosticCenter | Read | Read current/detail Diagnostic Center | export function GetDiagnosticCenter():Promise&lt;main.DiagnosticCenterSnapshot&gt;; |
| GetDiagnosticHistory | Read | Read current/detail Diagnostic History | export function GetDiagnosticHistory(arg1:number):Promise&lt;main.DiagnosticHistoryView&gt;; |
| GetDiagnosticSnapshot | Read | Read current/detail Diagnostic Snapshot | export function GetDiagnosticSnapshot(arg1:number):Promise&lt;main.DiagnosticCenterSnapshot&gt;; |
| GetSystemLogEventDetail | Read | Read current/detail System Log Event Detail | export function GetSystemLogEventDetail(arg1:string):Promise&lt;main.SystemLogEventDetail&gt;; |
| QuerySystemLog | Read | Query System Log | export function QuerySystemLog(arg1:logstore.EventQuery):Promise&lt;main.SystemLogPage&gt;; |
| RefreshCoreDiagnostics | Refresh | Refresh Core Diagnostics | export function RefreshCoreDiagnostics():Promise&lt;main.CoreDiagnostics&gt;; |
| RefreshDiagnosticCenter | Refresh | Refresh Diagnostic Center | export function RefreshDiagnosticCenter():Promise&lt;main.DiagnosticCenterSnapshot&gt;; |

## Recovery

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| CancelPendingRecoveryRestore | Mutation | Cancel Pending Recovery Restore | export function CancelPendingRecoveryRestore():Promise&lt;void&gt;; |
| ChooseRecoveryBackupFile | Desktop picker | Open desktop picker for Recovery Backup File | export function ChooseRecoveryBackupFile():Promise&lt;string&gt;; |
| ConfirmRecoveryCatalogQuarantine | Mutation | Confirm Recovery Catalog Quarantine | export function ConfirmRecoveryCatalogQuarantine(arg1:string,arg2:string):Promise&lt;recovery.BackupCatalogQuarantineResult&gt;; |
| ConfirmRecoveryRestore | Mutation | Confirm Recovery Restore | export function ConfirmRecoveryRestore(arg1:string,arg2:string):Promise&lt;recovery.RestoreArmResult&gt;; |
| ConfirmRecoveryRestoreDrill | Mutation | Confirm Recovery Restore Drill | export function ConfirmRecoveryRestoreDrill(arg1:string,arg2:string):Promise&lt;recovery.RestoreDrillResult&gt;; |
| CreateManagedRecoveryBackup | Mutation | Create Managed Recovery Backup | export function CreateManagedRecoveryBackup():Promise&lt;recovery.BackupRecord&gt;; |
| CreateRecoveryCatalogQuarantinePreflight | Mutation | Create Recovery Catalog Quarantine Preflight | export function CreateRecoveryCatalogQuarantinePreflight(arg1:string,arg2:string):Promise&lt;recovery.BackupCatalogQuarantinePreflight&gt;; |
| CreateRecoveryCatalogReleasePreflight | Mutation | Create Recovery Catalog Release Preflight | export function CreateRecoveryCatalogReleasePreflight(arg1:string):Promise&lt;recovery.BackupCatalogQuarantinePreflight&gt;; |
| CreateRecoveryRestoreDrillPreflight | Mutation | Create Recovery Restore Drill Preflight | export function CreateRecoveryRestoreDrillPreflight(arg1:string):Promise&lt;recovery.RestoreDrillPreflight&gt;; |
| CreateRecoveryRestorePreflight | Mutation | Create Recovery Restore Preflight | export function CreateRecoveryRestorePreflight(arg1:string):Promise&lt;recovery.RestorePreflight&gt;; |
| ExportRecoveryReadinessReport | File export | Export Recovery Readiness Report | export function ExportRecoveryReadinessReport():Promise&lt;recovery.RecoveryReadinessExportResult&gt;; |
| GetRecoveryBackupAutomation | Read | Read current/detail Recovery Backup Automation | export function GetRecoveryBackupAutomation():Promise&lt;recovery.BackupAutomationView&gt;; |
| GetRecoveryOverview | Read | Read current/detail Recovery Overview | export function GetRecoveryOverview():Promise&lt;recovery.RecoveryOverview&gt;; |
| RunRecoveryBackupCatalogHealth | Controlled operation | Run controlled Recovery Backup Catalog Health | export function RunRecoveryBackupCatalogHealth(arg1:boolean):Promise&lt;recovery.BackupCatalogHealth&gt;; |
| RunRecoveryBackupScheduleNow | Controlled operation | Run controlled Recovery Backup Schedule Now | export function RunRecoveryBackupScheduleNow():Promise&lt;recovery.BackupSchedulerRunResult&gt;; |
| RunRecoveryIntegrityCheck | Controlled operation | Run controlled Recovery Integrity Check | export function RunRecoveryIntegrityCheck(arg1:boolean):Promise&lt;recovery.IntegrityResult&gt;; |
| RunRecoveryReadinessGate | Controlled operation | Run controlled Recovery Readiness Gate | export function RunRecoveryReadinessGate():Promise&lt;recovery.RecoveryReadinessSnapshot&gt;; |
| UpdateRecoveryBackupAutomation | Mutation | Update Recovery Backup Automation | export function UpdateRecoveryBackupAutomation(arg1:boolean,arg2:number,arg3:number,arg4:number):Promise&lt;recovery.BackupAutomationView&gt;; |
| ValidateRecoveryBackup | Mutation | Validate Validate Recovery Backup | export function ValidateRecoveryBackup(arg1:string):Promise&lt;recovery.BackupValidation&gt;; |

## Legacy Import

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ChooseLegacyProjectRoot | Desktop picker | Open desktop picker for Legacy Project Root | export function ChooseLegacyProjectRoot():Promise&lt;string&gt;; |
| ImportLegacyProject | Mutation | Import Legacy Project | export function ImportLegacyProject(arg1:string):Promise&lt;legacyimport.FullImportResult&gt;; |

## Other

| Method | Class | Semantic | Exact TypeScript signature |
|---|---|---|---|
| ConfirmManagedBackupLifecycle | Mutation | Confirm Managed Backup Lifecycle | export function ConfirmManagedBackupLifecycle(arg1:string,arg2:string):Promise&lt;recovery.BackupLifecycleResult&gt;; |
| PreviewDocumentsCatchUp | Preview / advisory | Preview/validate without commit Documents Catch Up | export function PreviewDocumentsCatchUp(arg1:number):Promise&lt;coredb.DocumentsCatchUpPreview&gt;; |

## Safety notes for high-risk API families

### Campaign / Preflight / Dispatch

Create/Update campaign methods operate on mutable authoring state. Preflight Create methods create durable evidence stages. CreateCampaignDispatchSnapshot crosses the immutable freeze boundary. GetCampaignDispatchHandoff is the final read-side readiness projection before send orchestration.

### Queue / Attempt

CreateSendQueue creates persistent execution state but does not imply delivery. Start/Pause/Resume/Cancel control Queue orchestration. RetrySendQueueItemNow is not a force-resend override; retry eligibility remains a Core rule.

### SMTP

TestSMTPProfileConnection is connectivity evidence. SendDispatchRecipientSMTP crosses the real transport boundary and remains subject to runtime/profile/controlled-send guards.

### DSN / Inbound

ScanInboundMailbox performs bounded read-only mailbox intake. DSN manual reconciliation uses Preview then Confirm; original automatic correlation evidence is not rewritten.

### Recovery

Recovery preflight and confirmation methods are deliberately separate. Do not collapse preview/arm/confirm boundaries in frontend code.

### Module execution

ExecuteModule invokes a capability through ModuleHost and stable ABI rules; it must not be treated as arbitrary DLL execution.

## API evolution rule

When an exported App method changes:

1. update the Go implementation;
2. regenerate Wails bindings;
3. update frontend callers;
4. run typecheck/tests;
5. update this reference if the binding surface changed;
6. run the current acceptance gate;
7. bump the documented source SHA only after documentation review.
