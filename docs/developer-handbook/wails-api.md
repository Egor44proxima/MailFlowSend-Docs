# Wails API

MailFlowSend exposes one Wails-bound Go object: `*main.App`.

The generated TypeScript declaration file at `frontend/wailsjs/go/main/App.d.ts` is the practical frontend contract. At the source snapshot documented by this handbook it exports **242 functions**.

## Binding path

~~~mermaid
flowchart LR
    Vue["Vue component"] --> JS["frontend/wailsjs/go/main/App.js"]
    JS --> Wails["Wails runtime bridge"]
    Wails --> App["exported method on *main.App"]
    App --> Core["CoreDB / internal package / worker"]
~~~

## Rules for API evolution

- Wails method names are operator/frontend contracts; renaming them is a breaking frontend change.
- Use typed CoreDB/internal model return values where possible.
- Long-running business logic should not be implemented in Vue.
- File-picker methods may return local paths to the trusted desktop UI, but paths/secrets should not be copied into structured logs or public diagnostic bundles.
- Mutation methods should perform server-side validation even when the UI disables an invalid action.
- Read-only methods should not hide business-state mutation behind a query/refresh name.
- Generated `wailsjs` files are outputs; the Go source method is authoritative.

## Domain map

| Domain | Representative methods |
|---|---|
| Core/runtime | `GetCoreStatus`, `GetCoreDiagnostics`, `GetRuntimeSafety` |
| Clients/CSM | `GetClient`, `ListClientRegistryFiltered`, `TransferClientCSM`, `SetClientCooperationStatus` |
| Attachments | `IndexAttachmentBatch`, `RunAttachmentMatcher`, `ProbeUnavailableAttachment` |
| GENERAL registry | `ListMailingContacts`, `AddMailingContact`, taxonomy/import methods |
| Campaign/preflight | `CreateCampaignDraft`, `CreateCampaignPreflight*`, `CreateCampaignDispatchSnapshot` |
| Debt | `CreateDebtImportSnapshot`, `GetDebtImportSnapshot` |
| SMTP | `ListSMTPProfiles`, `TestSMTPProfileConnection`, `SendDispatchRecipientSMTP` |
| Queue | `CreateSendQueue`, `StartSendQueue`, `PauseSendQueue`, `RetrySendQueueItemNow` |
| Delivery/History | `QueryDeliveryHistoryWorkspace`, `GetDeliveryHistoryDetail`, `ExportDeliveryHistoryConfigured` |
| DSN | `ListDSNArtifacts`, `GetDSNArtifactDetail`, manual reconciliation methods |
| Inbound | `ScanInboundMailbox`, mailbox profile/scheduler methods |
| Diagnostics | `GetDiagnosticCenter`, `ExportDiagnosticAIBundle` |
| Logging | `QuerySystemLog`, `GetSystemLogEventDetail` |
| Recovery | backup/catalog/readiness/drill/restore methods |
| Modules | `GetModuleSnapshot`, `RefreshModules`, `ExecuteModule` |
| Template control | `GetTemplateEngineStatus`, `SetTemplateEngineSpintaxEnabled` |

## Return-type namespaces

Generated bindings currently reference models from:

~~~text
coredb
inboundmailbox
main
recovery
smtpcredential
modulehost
legacyimport
logstore
mailtransport
~~~

This mirrors the Go package boundary visible to the Wails generator.

## Full generated method inventory

The signatures below are copied from the generated binding for the documented source snapshot. Argument names such as `arg1` are generated and should not be treated as semantic documentation; inspect the Go method for business meaning.

~~~typescript
AddClientContact(arg1:number,arg2:string,arg3:boolean,arg4:string):Promise<coredb.ClientContactMutationResult>;
AddDebtCampaignAttachments(arg1:number,arg2:Array<string>):Promise<coredb.CampaignDetail>;
AddGeneralCampaignAttachments(arg1:number,arg2:Array<string>):Promise<coredb.CampaignDetail>;
AddInboundMailboxProfile(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string):Promise<inboundmailbox.ProfileMutationResult>;
AddMailingContact(arg1:string,arg2:string,arg3:string,arg4:string):Promise<coredb.MailingContactMutationResult>;
AddMailingGroup(arg1:string,arg2:string):Promise<coredb.MailingTaxonomyMutationResult>;
AddMailingTag(arg1:string,arg2:string):Promise<coredb.MailingTaxonomyMutationResult>;
AddSMTPProfile(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:number):Promise<coredb.SMTPProfileMutationResult>;
AddSMTPProfileV2(arg1:string,arg2:string,arg3:string,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:number):Promise<coredb.SMTPProfileMutationResult>;
AddSenderProfile(arg1:string,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string,arg7:string):Promise<coredb.SenderProfileMutationResult>;
CancelPendingRecoveryRestore():Promise<void>;
CancelSendQueue(arg1:number):Promise<coredb.SendQueueJobView>;
CaptureDiagnosticSnapshot():Promise<main.DiagnosticHistoryCaptureResult>;
ChooseAttachmentBatchFolder():Promise<string>;
ChooseDSNArtifactFile():Promise<string>;
ChooseDebtCampaignAttachments():Promise<Array<string>>;
ChooseDebtImportFile():Promise<string>;
ChooseGeneralCampaignAttachments():Promise<Array<string>>;
ChooseLegacyProjectRoot():Promise<string>;
ChooseMailingContactImportFile():Promise<string>;
ChooseRecoveryBackupFile():Promise<string>;
ClassifyAttachmentOrphans(arg1:number):Promise<coredb.OrphanClassificationSummary>;
CommitMailingContactImport(arg1:string,arg2:string,arg3:coredb.MailingImportMapping,arg4:string,arg5:string,arg6:Array<number>,arg7:Array<number>):Promise<coredb.MailingContactImportResult>;
ConfirmDSNManualReconciliation(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:boolean):Promise<coredb.DSNManualReconciliationResult>;
ConfirmManagedBackupLifecycle(arg1:string,arg2:string):Promise<recovery.BackupLifecycleResult>;
ConfirmRecoveryCatalogQuarantine(arg1:string,arg2:string):Promise<recovery.BackupCatalogQuarantineResult>;
ConfirmRecoveryRestore(arg1:string,arg2:string):Promise<recovery.RestoreArmResult>;
ConfirmRecoveryRestoreDrill(arg1:string,arg2:string):Promise<recovery.RestoreDrillResult>;
CreateCampaignDispatchSnapshot(arg1:number):Promise<coredb.CampaignDispatchSnapshotView>;
CreateCampaignDraft(arg1:string,arg2:number,arg3:string,arg4:Array<number>,arg5:string,arg6:string,arg7:string):Promise<coredb.CampaignDetail>;
CreateCampaignPreflightAttachmentResolution(arg1:number):Promise<coredb.CampaignPreflightAttachmentResolutionView>;
CreateCampaignPreflightEligibility(arg1:number):Promise<coredb.CampaignPreflightEligibilityView>;
CreateCampaignPreflightFoundation(arg1:number):Promise<coredb.CampaignPreflightFoundationView>;
CreateCampaignPreflightRecipientResolution(arg1:number):Promise<coredb.CampaignPreflightRecipientResolutionView>;
CreateClientFromMissingOrphan(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:string,arg7:string,arg8:string,arg9:boolean):Promise<coredb.ClientRegistryIntakeResult>;
CreateDebtImportSnapshot(arg1:string,arg2:string,arg3:number,arg4:Record<string, number>):Promise<coredb.DebtImportSnapshotResult>;
CreateDebtNoticeCampaignDraft(arg1:string,arg2:number,arg3:string,arg4:string,arg5:string,arg6:string):Promise<coredb.CampaignDetail>;
CreateDocumentsCatchUpCampaign(arg1:number):Promise<coredb.DocumentsCatchUpCreateResult>;
CreateGeneralCampaignDraft(arg1:string,arg2:Array<number>,arg3:Array<number>,arg4:number,arg5:string,arg6:string,arg7:string,arg8:string):Promise<coredb.CampaignDetail>;
CreateManagedBackupLifecyclePreflight(arg1:string,arg2:string):Promise<recovery.BackupLifecyclePreflight>;
CreateManagedRecoveryBackup():Promise<recovery.BackupRecord>;
CreateRecoveryCatalogQuarantinePreflight(arg1:string,arg2:string):Promise<recovery.BackupCatalogQuarantinePreflight>;
CreateRecoveryCatalogReleasePreflight(arg1:string):Promise<recovery.BackupCatalogQuarantinePreflight>;
CreateRecoveryRestoreDrillPreflight(arg1:string):Promise<recovery.RestoreDrillPreflight>;
CreateRecoveryRestorePreflight(arg1:string):Promise<recovery.RestorePreflight>;
CreateSendQueue(arg1:number,arg2:number,arg3:number,arg4:number,arg5:number,arg6:number):Promise<coredb.SendQueueDetail>;
DeactivateClientContact(arg1:number,arg2:string):Promise<coredb.ClientContactMutationResult>;
DeferMissingClientVerification(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string):Promise<coredb.ReconciliationResult>;
DeleteInboundMailboxCredential(arg1:number):Promise<inboundmailbox.CredentialMutationResult>;
DeleteSMTPProfileCredential(arg1:number):Promise<smtpcredential.MutationResult>;
DismissReconciliationCase(arg1:number,arg2:string):Promise<coredb.ReconciliationResult>;
ExcludeCampaignEligibilityBlocked(arg1:number,arg2:number):Promise<coredb.CampaignEligibilityBlockedExclusionResult>;
ExecuteModule(arg1:string,arg2:string):Promise<main.ExecuteResult>;
ExportDeliveryHistory(arg1:coredb.DeliveryHistoryWorkspaceQuery,arg2:string):Promise<string>;
ExportDeliveryHistoryConfigured(arg1:coredb.DeliveryHistoryWorkspaceQuery,arg2:string,arg3:Array<string>):Promise<string>;
ExportDiagnosticAIBundle():Promise<main.DiagnosticAIBundleExportResult>;
ExportRecoveryReadinessReport():Promise<recovery.RecoveryReadinessExportResult>;
GetAttachmentMatchSummary(arg1:number):Promise<coredb.AttachmentMatchSummary>;
GetBounceDeliveryIntelligence(arg1:number,arg2:string):Promise<coredb.BounceDeliveryIntelligenceSnapshot>;
GetCampaign(arg1:number):Promise<coredb.CampaignDetail>;
GetCampaignDispatchHandoff(arg1:number):Promise<coredb.CampaignDispatchHandoffView>;
GetCampaignDispatchSnapshot(arg1:number):Promise<coredb.CampaignDispatchSnapshotView>;
GetCampaignPreflightAttachmentResolution(arg1:number):Promise<coredb.CampaignPreflightAttachmentResolutionView>;
GetCampaignPreflightEligibility(arg1:number):Promise<coredb.CampaignPreflightEligibilityView>;
GetCampaignPreflightFoundation(arg1:number):Promise<coredb.CampaignPreflightFoundationView>;
GetCampaignPreflightRecipientResolution(arg1:number):Promise<coredb.CampaignPreflightRecipientResolutionView>;
GetClient(arg1:number):Promise<coredb.ClientDetail>;
GetClientMonthActivity(arg1:string,arg2:string):Promise<coredb.ClientMonthActivityProjection>;
GetClientMonthEvidence(arg1:number,arg2:string):Promise<coredb.ClientMonthEvidenceView>;
GetClientMonthSignals(arg1:string,arg2:string):Promise<coredb.ClientMonthSignalProjection>;
GetClientRegistryQualityDetails(arg1:number):Promise<coredb.ClientRegistryQualityDetails>;
GetCoreDiagnostics():Promise<main.CoreDiagnostics>;
GetCoreStatus():Promise<coredb.Status>;
GetDSNArtifactDetail(arg1:number):Promise<coredb.DSNArtifactDetail>;
GetDSNMessageIDDiagnostics(arg1:number):Promise<coredb.DSNMessageIDDiagnosticsView>;
GetDebtImportSnapshot(arg1:number):Promise<coredb.DebtImportSnapshotResult>;
GetDeliveryHistoryDetail(arg1:number):Promise<coredb.DeliveryHistoryDetail>;
GetDeliveryHistorySummary():Promise<coredb.DeliveryHistorySummary>;
GetDeliveryUnknownReviewDetail(arg1:number):Promise<coredb.DeliveryUnknownReviewDetail>;
GetDiagnosticCenter():Promise<main.DiagnosticCenterSnapshot>;
GetDiagnosticHistory(arg1:number):Promise<main.DiagnosticHistoryView>;
GetDiagnosticSnapshot(arg1:number):Promise<main.DiagnosticCenterSnapshot>;
GetDocumentsMonthlyCoverage(arg1:number):Promise<coredb.DocumentsMonthlyCoverageView>;
GetInboundMailboxCredentialStatus(arg1:number):Promise<inboundmailbox.CredentialStatus>;
GetInboundMailboxScanProgress(arg1:number):Promise<inboundmailbox.ScanProgress>;
GetInboundMailboxScanSchedule(arg1:number):Promise<coredb.InboundMailboxScanScheduleView>;
GetInboundMailboxScanState(arg1:number):Promise<coredb.InboundMailboxScanStateView>;
GetInboundMonitoringAlerts(arg1:number):Promise<coredb.InboundMonitoringSnapshot>;
GetModuleSnapshot():Promise<modulehost.Snapshot>;
GetOrphanClassificationSummary(arg1:number):Promise<coredb.OrphanClassificationSummary>;
GetReconciliationSummary(arg1:number):Promise<coredb.ReconciliationSummary>;
GetRecoveryBackupAutomation():Promise<recovery.BackupAutomationView>;
GetRecoveryOverview():Promise<recovery.RecoveryOverview>;
GetRuntimeSafety():Promise<main.RuntimeSafetyView>;
GetSMTPProfileCredentialStatus(arg1:number):Promise<smtpcredential.Status>;
GetSMTPSessionDetail(arg1:number):Promise<coredb.SMTPSessionDetail>;
GetSendQueueDetail(arg1:number):Promise<coredb.SendQueueDetail>;
GetSystemLogEventDetail(arg1:string):Promise<main.SystemLogEventDetail>;
GetTemplateEngineStatus():Promise<coredb.TemplateEngineStatusView>;
ImportLegacyProject(arg1:string):Promise<legacyimport.FullImportResult>;
IndexAttachmentBatch(arg1:string):Promise<coredb.AttachmentBatchView>;
IngestDSNArtifactFile(arg1:string):Promise<coredb.DSNIngestionResult>;
InspectMailingContactImport(arg1:string,arg2:string):Promise<coredb.MailingContactImportInspection>;
ListAttachmentBatches():Promise<Array<coredb.AttachmentBatchView>>;
ListAttachmentMatchResults(arg1:number,arg2:string):Promise<Array<coredb.AttachmentMatchView>>;
ListAttachmentPeriodCounts(arg1:number):Promise<Array<coredb.PeriodCount>>;
ListAttachmentResolutionEvents(arg1:number):Promise<Array<coredb.AttachmentResolutionEventView>>;
ListAttachments(arg1:number,arg2:string):Promise<Array<coredb.AttachmentView>>;
ListBouncedRecipientReviews(arg1:number):Promise<Array<coredb.BouncedRecipientReviewView>>;
ListCSMs():Promise<Array<coredb.CSMView>>;
ListCampaignDispatchSnapshots(arg1:number,arg2:number):Promise<Array<coredb.CampaignDispatchSnapshotView>>;
ListCampaignEvents(arg1:number):Promise<Array<coredb.CampaignEventView>>;
ListCampaignPreflightAttachmentResolutions(arg1:number,arg2:number):Promise<Array<coredb.CampaignPreflightAttachmentResolutionView>>;
ListCampaignPreflightEligibilities(arg1:number,arg2:number):Promise<Array<coredb.CampaignPreflightEligibilityView>>;
ListCampaignPreflightFoundations(arg1:number,arg2:number):Promise<Array<coredb.CampaignPreflightFoundationView>>;
ListCampaignPreflightRecipientResolutions(arg1:number,arg2:number):Promise<Array<coredb.CampaignPreflightRecipientResolutionView>>;
ListCampaignTemplatePreviewRecipients(arg1:number):Promise<Array<coredb.CampaignTemplatePreviewRecipientView>>;
ListCampaigns():Promise<Array<coredb.CampaignSummary>>;
ListClientAttachmentBatchStates(arg1:number,arg2:string):Promise<Array<coredb.ClientAttachmentBatchStateView>>;
ListClientCSMTransferEvents(arg1:number):Promise<Array<coredb.ClientCSMTransferEventView>>;
ListClientContactEvents(arg1:number):Promise<Array<coredb.ClientContactEventView>>;
ListClientCooperationStatusEvents(arg1:number):Promise<Array<coredb.ClientCooperationStatusEventView>>;
ListClientRegistry(arg1:string,arg2:number,arg3:number,arg4:number):Promise<coredb.ClientRegistryPage>;
ListClientRegistryFiltered(arg1:string,arg2:number,arg3:string,arg4:number,arg5:number):Promise<coredb.ClientRegistryPage>;
ListClientRegistryIntakeEvents(arg1:number):Promise<Array<coredb.ClientRegistryIntakeEventView>>;
ListClientRegistryQuality(arg1:string,arg2:number,arg3:string,arg4:string,arg5:number,arg6:number):Promise<coredb.ClientRegistryQualityPage>;
ListClients(arg1:string,arg2:number):Promise<Array<coredb.ClientView>>;
ListDSNArtifacts(arg1:string,arg2:number):Promise<Array<coredb.DSNArtifactView>>;
ListDebtImports(arg1:number):Promise<Array<coredb.DebtImportView>>;
ListDebtReconciliationCases(arg1:string):Promise<Array<coredb.DebtReconciliationCaseView>>;
ListDeliveryHistory(arg1:number,arg2:string,arg3:number):Promise<Array<coredb.DeliveryRecordView>>;
ListDeliveryUnknownReviews(arg1:number,arg2:string):Promise<Array<coredb.DeliveryUnknownReviewView>>;
ListInboundMailboxConnectionTests(arg1:number,arg2:number):Promise<Array<inboundmailbox.ConnectionTestResult>>;
ListInboundMailboxProfileEvents(arg1:number):Promise<Array<inboundmailbox.ProfileEvent>>;
ListInboundMailboxProfiles():Promise<Array<inboundmailbox.InboundMailboxProfile>>;
ListInboundMailboxScanItems(arg1:number,arg2:number):Promise<Array<coredb.InboundMailboxScanItemView>>;
ListInboundMailboxScans(arg1:number,arg2:number):Promise<Array<coredb.InboundMailboxScanView>>;
ListInboundMailboxScheduleEvents(arg1:number,arg2:number):Promise<Array<coredb.InboundMailboxScheduleEventView>>;
ListInboundMailboxScheduleRuns(arg1:number,arg2:number):Promise<Array<coredb.InboundMailboxScheduleRunView>>;
ListMailingContactEvents(arg1:number):Promise<Array<coredb.MailingContactEventView>>;
ListMailingContactImports(arg1:number):Promise<Array<coredb.MailingContactImportHistoryView>>;
ListMailingContacts():Promise<Array<coredb.MailingContactView>>;
ListMailingGroups():Promise<Array<coredb.MailingGroupView>>;
ListMailingTags():Promise<Array<coredb.MailingTagView>>;
ListMailingTaxonomyEvents(arg1:string,arg2:number):Promise<Array<coredb.MailingTaxonomyEventView>>;
ListOrphanClassifications(arg1:number,arg2:string):Promise<Array<coredb.OrphanClassificationView>>;
ListReconciliationCases(arg1:number,arg2:string):Promise<Array<coredb.ReconciliationCaseView>>;
ListSMTPProfileEvents(arg1:number):Promise<Array<coredb.SMTPProfileEventView>>;
ListSMTPProfiles():Promise<Array<coredb.SMTPProfileView>>;
ListSMTPSessions(arg1:number,arg2:number):Promise<Array<coredb.SMTPSessionView>>;
ListSendAttempts(arg1:number):Promise<Array<coredb.SendAttemptView>>;
ListSendQueues(arg1:number):Promise<Array<coredb.SendQueueJobView>>;
ListSenderProfileEvents(arg1:number):Promise<Array<coredb.SenderProfileEventView>>;
ListSenderProfiles():Promise<Array<coredb.SenderProfileView>>;
ListUnavailableAttachmentIssues(arg1:number,arg2:number):Promise<coredb.AttachmentAvailabilityIssuePage>;
OpenCoreDatabaseFolder():Promise<void>;
OpenUnavailableAttachmentFolder(arg1:number):Promise<void>;
PauseSendQueue(arg1:number):Promise<coredb.SendQueueJobView>;
PreflightLegacyProject(arg1:string):Promise<legacyimport.FullImportPreflight>;
PrepareBouncedRecipientResend(arg1:number):Promise<coredb.BounceResendCreateResult>;
PreviewAliasLearning(arg1:number,arg2:number,arg3:number,arg4:string):Promise<coredb.AliasLearningPreview>;
PreviewCampaignTemplateRecipient(arg1:coredb.CampaignTemplatePreviewRequest):Promise<coredb.CampaignTemplatePreviewView>;
PreviewClientCSMTransfer(arg1:number,arg2:number):Promise<coredb.ClientCSMTransferPreview>;
PreviewClientCooperationStatusChange(arg1:number,arg2:string):Promise<coredb.ClientCooperationStatusPreview>;
PreviewDSNManualReconciliation(arg1:number,arg2:number,arg3:number):Promise<coredb.DSNManualReconciliationPreview>;
PreviewDebtCampaignRecipient(arg1:number,arg2:number):Promise<coredb.DebtCampaignRecipientPreview>;
PreviewDebtCampaignRecipientIdentity(arg1:number,arg2:number,arg3:string):Promise<coredb.DebtCampaignRecipientPreview>;
PreviewDocumentsCatchUp(arg1:number):Promise<coredb.DocumentsCatchUpPreview>;
PreviewGeneralCampaignRecipient(arg1:number,arg2:number):Promise<coredb.GeneralCampaignRecipientPreview>;
PreviewMailingContactImport(arg1:string,arg2:string,arg3:coredb.MailingImportMapping,arg4:string,arg5:Array<number>,arg6:Array<number>):Promise<coredb.MailingContactImportPreview>;
PreviewMissingClientIntake(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string,arg6:string,arg7:string):Promise<coredb.ClientRegistryIntakePreview>;
ProbeUnavailableAttachment(arg1:number):Promise<coredb.AttachmentAvailabilityProbe>;
QueryDeliveryHistoryWorkspace(arg1:coredb.DeliveryHistoryWorkspaceQuery):Promise<coredb.DeliveryHistoryWorkspacePage>;
QuerySystemLog(arg1:logstore.EventQuery):Promise<main.SystemLogPage>;
ReactivateClientContact(arg1:number,arg2:boolean,arg3:string):Promise<coredb.ClientContactMutationResult>;
ReconcileDSNDeliveryProjection():Promise<coredb.DSNDeliveryProjectionResult>;
RefreshCoreDiagnostics():Promise<main.CoreDiagnostics>;
RefreshCoreStatus():Promise<coredb.Status>;
RefreshDiagnosticCenter():Promise<main.DiagnosticCenterSnapshot>;
RefreshModules():Promise<modulehost.Snapshot>;
RemoveDebtCampaignAttachment(arg1:number,arg2:number):Promise<coredb.CampaignDetail>;
RemoveGeneralCampaignAttachment(arg1:number,arg2:number):Promise<coredb.CampaignDetail>;
RemoveManualAttachmentResolution(arg1:number,arg2:number,arg3:string):Promise<coredb.OrphanResolutionResult>;
ResolveDebtReconciliationCase(arg1:number,arg2:number,arg3:string):Promise<coredb.DebtReconciliationResult>;
ResolveDeliveryUnknownReview(arg1:number,arg2:string,arg3:string):Promise<coredb.DeliveryUnknownReviewDetail>;
ResolveOrphanManual(arg1:number,arg2:number,arg3:number,arg4:string):Promise<coredb.OrphanResolutionResult>;
ResolveOrphanWithAlias(arg1:number,arg2:number,arg3:number,arg4:string,arg5:string):Promise<coredb.OrphanResolutionResult>;
ResumeSendQueue(arg1:number):Promise<coredb.SendQueueJobView>;
RetrySendQueueItemNow(arg1:number):Promise<coredb.SendQueueItemView>;
RunAttachmentMatcher(arg1:number):Promise<coredb.AttachmentMatchSummary>;
RunDebtClientMatching(arg1:string,arg2:string,arg3:number,arg4:Record<string, number>):Promise<coredb.DebtMatchingResult>;
RunRecoveryBackupCatalogHealth(arg1:boolean):Promise<recovery.BackupCatalogHealth>;
RunRecoveryBackupScheduleNow():Promise<recovery.BackupSchedulerRunResult>;
RunRecoveryIntegrityCheck(arg1:boolean):Promise<recovery.IntegrityResult>;
RunRecoveryReadinessGate():Promise<recovery.RecoveryReadinessSnapshot>;
ScanInboundMailbox(arg1:number,arg2:number):Promise<coredb.InboundMailboxScanResult>;
SearchDebtClientCandidates(arg1:string,arg2:number):Promise<Array<coredb.DebtClientCandidate>>;
SearchExistingClientsForMissingOrphan(arg1:number,arg2:number,arg3:string,arg4:number):Promise<coredb.ExistingClientSearchResponse>;
SendDispatchRecipientSMTP(arg1:number,arg2:number,arg3:number,arg4:boolean):Promise<mailtransport.Response>;
SendDispatchRecipientToMailpit(arg1:number,arg2:number,arg3:number):Promise<mailtransport.Response>;
SetAttachmentExpectedPeriod(arg1:number,arg2:string):Promise<coredb.AttachmentBatchView>;
SetCampaignAudienceAll(arg1:number,arg2:boolean):Promise<coredb.CampaignDetail>;
SetCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise<coredb.CampaignDetail>;
SetClientCooperationStatus(arg1:number,arg2:string,arg3:string):Promise<coredb.ClientCooperationStatusResult>;
SetDebtCampaignAudienceAll(arg1:number,arg2:boolean):Promise<coredb.CampaignDetail>;
SetDebtCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise<coredb.CampaignDetail>;
SetGeneralCampaignAudienceAll(arg1:number,arg2:boolean):Promise<coredb.CampaignDetail>;
SetGeneralCampaignAudienceIncluded(arg1:number,arg2:number,arg3:boolean):Promise<coredb.CampaignDetail>;
SetInboundMailboxCredential(arg1:number,arg2:string):Promise<inboundmailbox.CredentialMutationResult>;
SetInboundMailboxProfileActive(arg1:number,arg2:boolean,arg3:string):Promise<inboundmailbox.ProfileMutationResult>;
SetMailingContactGroup(arg1:number,arg2:number,arg3:boolean):Promise<coredb.MailingMembershipMutationResult>;
SetMailingContactStatus(arg1:number,arg2:string,arg3:string):Promise<coredb.MailingContactMutationResult>;
SetMailingContactTag(arg1:number,arg2:number,arg3:boolean):Promise<coredb.MailingMembershipMutationResult>;
SetMailingContactsGroup(arg1:Array<number>,arg2:number,arg3:boolean):Promise<coredb.MailingBulkMembershipResult>;
SetMailingContactsTag(arg1:Array<number>,arg2:number,arg3:boolean):Promise<coredb.MailingBulkMembershipResult>;
SetMailingGroupActive(arg1:number,arg2:boolean):Promise<coredb.MailingTaxonomyMutationResult>;
SetMailingTagActive(arg1:number,arg2:boolean):Promise<coredb.MailingTaxonomyMutationResult>;
SetPrimaryClientContact(arg1:number,arg2:string):Promise<coredb.ClientContactMutationResult>;
SetSMTPProfileActive(arg1:number,arg2:boolean,arg3:string):Promise<coredb.SMTPProfileMutationResult>;
SetSMTPProfileCredential(arg1:number,arg2:string):Promise<smtpcredential.MutationResult>;
SetSenderProfileActive(arg1:number,arg2:boolean,arg3:string):Promise<coredb.SenderProfileMutationResult>;
SetTemplateEngineSpintaxEnabled(arg1:boolean):Promise<coredb.TemplateEngineStatusView>;
StartSendQueue(arg1:number,arg2:boolean):Promise<coredb.SendQueueJobView>;
SuggestAttachmentAlias(arg1:string):Promise<string>;
TestInboundMailboxConnection(arg1:number):Promise<inboundmailbox.ConnectionTestResult>;
TestSMTPProfileConnection(arg1:number):Promise<mailtransport.Response>;
TransferClientCSM(arg1:number,arg2:number,arg3:string):Promise<coredb.ClientCSMTransferResult>;
UpdateCampaignDraft(arg1:number,arg2:string,arg3:number,arg4:string,arg5:Array<number>,arg6:string,arg7:string,arg8:string):Promise<coredb.CampaignDetail>;
UpdateClientContact(arg1:number,arg2:string,arg3:boolean,arg4:string):Promise<coredb.ClientContactMutationResult>;
UpdateDebtNoticeCampaignDraft(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string):Promise<coredb.CampaignDetail>;
UpdateGeneralCampaignDraft(arg1:number,arg2:string,arg3:Array<number>,arg4:Array<number>,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string):Promise<coredb.CampaignDetail>;
UpdateInboundMailboxProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string):Promise<inboundmailbox.ProfileMutationResult>;
UpdateInboundMailboxScanSchedule(arg1:number,arg2:boolean,arg3:number,arg4:number):Promise<coredb.InboundMailboxScanScheduleMutationResult>;
UpdateMailingContact(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string):Promise<coredb.MailingContactMutationResult>;
UpdateMailingGroup(arg1:number,arg2:string,arg3:string):Promise<coredb.MailingTaxonomyMutationResult>;
UpdateMailingTag(arg1:number,arg2:string,arg3:string):Promise<coredb.MailingTaxonomyMutationResult>;
UpdateReconciliationCase(arg1:number,arg2:number,arg3:string):Promise<coredb.ReconciliationResult>;
UpdateRecoveryBackupAutomation(arg1:boolean,arg2:number,arg3:number,arg4:number):Promise<recovery.BackupAutomationView>;
UpdateSMTPProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:number):Promise<coredb.SMTPProfileMutationResult>;
UpdateSMTPProfileV2(arg1:number,arg2:string,arg3:string,arg4:string,arg5:number,arg6:string,arg7:string,arg8:string,arg9:string,arg10:string,arg11:string,arg12:string,arg13:number):Promise<coredb.SMTPProfileMutationResult>;
UpdateSenderProfile(arg1:number,arg2:string,arg3:string,arg4:string,arg5:string,arg6:string,arg7:string,arg8:string):Promise<coredb.SenderProfileMutationResult>;
ValidateRecoveryBackup(arg1:string):Promise<recovery.BackupValidation>;
~~~

## Adding a new Wails method

Recommended sequence:

1. add/export the method on `*App`;
2. keep business logic in Core/internal owner;
3. validate all mutation inputs in Go;
4. return a stable typed result or bounded JSON contract;
5. regenerate Wails bindings through the normal build;
6. run frontend typecheck;
7. add backend tests;
8. add frontend tests when async/state behavior changes;
9. run current acceptance gate.

## Async frontend rule

Vue must treat Wails calls as asynchronous external state reads/mutations. The current frontend includes helpers/tests for:

- latest-request wins semantics;
- event subscription lifecycle;
- Queue workspace model decomposition;
- History export model behavior.

Do not assume response order equals request order when multiple refreshes are in flight.
