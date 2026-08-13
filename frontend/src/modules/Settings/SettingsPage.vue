<template>
  <q-page class="settings-page">
    <div class="settings-header">
      <div>
        <div class="eyebrow">Profile settings</div>
        <h1>AI Actions</h1>
        <p>Connect a Custom GPT, n8n, or another trusted automation to CareerVault.</p>
      </div>
    </div>

    <q-tabs v-model="tab" dense align="left" active-color="primary" indicator-color="primary" class="settings-tabs">
      <q-tab name="keys" icon="key" label="API keys" />
      <q-tab name="docs" icon="menu_book" label="OpenAPI documentation" />
    </q-tabs>

    <q-tab-panels v-model="tab" animated class="settings-panels">
      <q-tab-panel name="keys" class="q-pa-none">
        <div class="panel-card intro-card">
          <div class="intro-icon"><q-icon name="security" size="24px" /></div>
          <div>
            <div class="card-title">Private API access</div>
            <div class="card-copy">Keys are shown only once when created and stored securely as a hash. Revoke any key immediately if it is exposed.</div>
          </div>
          <q-space />
          <q-btn unelevated no-caps color="primary" icon="add" label="Create API key" @click="openCreate" />
        </div>

        <div v-if="newKey" class="panel-card reveal-card">
          <div class="reveal-heading"><q-icon name="check_circle" color="positive" /> API key created</div>
          <div class="card-copy">Copy this key now. For security, it will not be shown again.</div>
          <div class="key-reveal"><code>{{ newKey }}</code><q-btn flat round icon="content_copy" color="primary" @click="copy(newKey)"><q-tooltip>Copy API key</q-tooltip></q-btn></div>
          <q-btn flat no-caps label="I have saved it" @click="newKey = null" />
        </div>

        <div class="panel-card table-card">
          <q-table flat :rows="keys" :columns="columns" row-key="id" :loading="loading" no-data-label="No API keys created yet">
            <template #body-cell-key_prefix="props"><q-td :props="props"><code class="prefix">{{ props.row.key_prefix }}…</code></q-td></template>
            <template #body-cell-is_revoked="props"><q-td :props="props"><q-badge :color="props.row.is_revoked ? 'grey-6' : 'positive'" :label="props.row.is_revoked ? 'Revoked' : 'Active'" /></q-td></template>
            <template #body-cell-created_on_utc="props"><q-td :props="props">{{ formatDate(props.row.created_on_utc) }}</q-td></template>
            <template #body-cell-actions="props"><q-td :props="props" class="text-right"><q-btn v-if="!props.row.is_revoked" flat round dense icon="edit" color="primary" @click="openEdit(props.row)"><q-tooltip>Edit key</q-tooltip></q-btn><q-btn v-if="!props.row.is_revoked" flat round dense icon="block" color="negative" @click="revoke(props.row)"><q-tooltip>Revoke key</q-tooltip></q-btn></q-td></template>
          </q-table>
        </div>
      </q-tab-panel>

      <q-tab-panel name="docs" class="q-pa-none">
        <div class="panel-card docs-card">
          <div class="card-title">Connect your Custom GPT</div>
          <div class="card-copy">Use the API key as the <code>X-CareerVault-Key</code> header. All records are scoped to the user who owns the key. AI-created opportunities always start as Draft.</div>
          <div class="doc-block"><div class="doc-label">Backend base URL</div><div class="code-line"><code>{{ apiBaseUrl }}</code><q-btn flat round dense icon="content_copy" @click="copy(apiBaseUrl)" /></div></div>
          <div class="doc-block"><div class="doc-label">Authentication</div><pre>{{ authExample }}</pre><q-btn flat no-caps icon="content_copy" label="Copy" @click="copy(authExample)" /></div>
          <div class="doc-block"><div class="doc-label">OpenAPI actions</div><pre>{{ openApiExample }}</pre><q-btn flat no-caps icon="content_copy" label="Copy" @click="copy(openApiExample)" /></div>
          <q-banner rounded class="docs-note" icon="info"><span>For a Custom GPT, import <a :href="openApiUrl" target="_blank" rel="noopener">{{ openApiUrl }}</a> as the action schema, then configure an API key security scheme using the <code>X-CareerVault-Key</code> header.</span></q-banner>
          <q-separator class="q-my-lg" />
          <div class="card-title">Connect your n8n email agent</div>
          <div class="card-copy">Use the same generated key and <code>X-CareerVault-Key</code> header as AI Actions. The separate email-agent contract can search this user’s applications and record classified recruiter replies.</div>
          <div class="doc-block"><div class="doc-label">Email agent authentication</div><pre>{{ emailAuthExample }}</pre><q-btn flat no-caps icon="content_copy" label="Copy" @click="copy(emailAuthExample)" /></div>
          <div class="doc-block"><div class="doc-label">Email agent actions</div><pre>{{ emailApiExample }}</pre><q-btn flat no-caps icon="content_copy" label="Copy" @click="copy(emailApiExample)" /></div>
          <q-banner rounded class="docs-note" icon="mark_email_read"><span>Import <a :href="emailOpenApiUrl" target="_blank" rel="noopener">{{ emailOpenApiUrl }}</a> into the agent tool and configure its API-key header as <code>X-CareerVault-Key</code>.</span></q-banner>
        </div>
      </q-tab-panel>
    </q-tab-panels>

    <q-dialog v-model="createDialog">
      <q-card class="key-dialog">
        <q-card-section><div class="card-title">{{ editingId ? "Edit API key" : "Create API key" }}</div><div class="card-copy">Use a name that identifies the automation, such as “Job search GPT”.</div></q-card-section>
        <q-card-section><q-input v-model="form.name" outlined autofocus label="Key name *" :rules="[required]" /><q-input v-model="form.expires_on_utc" class="q-mt-md" outlined label="Expiration (optional)" type="date" /></q-card-section>
        <q-card-actions align="right"><q-btn flat no-caps label="Cancel" v-close-popup /><q-btn unelevated no-caps color="primary" :label="editingId ? 'Save changes' : 'Create key'" :loading="saving" @click="create" /></q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { apiKeyApi, type ApiKey } from "@/api/apiKeys";

const $q = useQuasar();
const tab = ref("keys");
const keys = ref<ApiKey[]>([]);
const loading = ref(false);
const saving = ref(false);
const createDialog = ref(false);
const newKey = ref<string | null>(null);
const editingId = ref<string | null>(null);
const form = reactive({ name: "", expires_on_utc: "" });
const columns: QTableProps["columns"] = [
  { name: "name", label: "Name", align: "left", field: "name" },
  { name: "key_prefix", label: "Key", align: "left", field: "key_prefix" },
  { name: "is_revoked", label: "Status", align: "left", field: "is_revoked" },
  { name: "created_on_utc", label: "Created", align: "left", field: "created_on_utc" },
  { name: "actions", label: "", align: "right", field: "id" }
];
const configuredBackendUrl = (import.meta.env.VITE_BACKEND_URL as string | undefined)
  || (import.meta.env.VITE_API_URL as string | undefined);
const backendOrigin = computed(() => {
  const value = configuredBackendUrl?.replace(/\/$/, "");
  if (value && /^https?:\/\//.test(value)) return value.replace(/\/api\/v1$/, "");
  return typeof window !== "undefined" ? window.location.origin : "http://localhost:8000";
});
const apiBaseUrl = computed(() => backendOrigin.value);
const openApiUrl = computed(() => `${backendOrigin.value}/api/v1/ai/openapi.json`);
const emailOpenApiUrl = computed(() => `${backendOrigin.value}/api/v1/email-agent/openapi.json`);
const authExample = `X-CareerVault-Key: cvai_your_key_here`;
const emailAuthExample = `X-CareerVault-Key: cvai_your_key_here`;
const openApiExample = `GET /api/v1/ai/opportunities?query=python&status=draft\nPOST /api/v1/ai/opportunities\nPOST /api/v1/ai/opportunities/bulk\nPATCH /api/v1/ai/opportunities/{id}  (draft only)\nDELETE /api/v1/ai/opportunities/{id}  (draft only)`;
const emailApiExample = `GET /api/v1/email-agent/applications?query=company-or-role\nPOST /api/v1/email-agent/follow-ups\nPATCH /api/v1/email-agent/follow-ups/{id}`;

function required(value: string) { return value.trim().length > 0 || "A name is required"; }
function formatDate(value: string) { return new Date(value).toLocaleDateString(); }
function openCreate() { editingId.value = null; form.name = ""; form.expires_on_utc = ""; createDialog.value = true; }
function openEdit(key: ApiKey) { editingId.value = key.id; form.name = key.name; form.expires_on_utc = key.expires_on_utc?.slice(0, 10) ?? ""; createDialog.value = true; }
async function load() { loading.value = true; try { keys.value = await apiKeyApi.list(); } catch { $q.notify({ type: "negative", message: "Could not load API keys" }); } finally { loading.value = false; } }
async function create() {
  if (!form.name.trim()) return;
  saving.value = true;
  try { if (editingId.value) { await apiKeyApi.update(editingId.value, { name: form.name.trim(), expires_on_utc: form.expires_on_utc ? `${form.expires_on_utc}T00:00:00Z` : null }); } else { const created = await apiKeyApi.create({ name: form.name.trim(), expires_on_utc: form.expires_on_utc ? `${form.expires_on_utc}T00:00:00Z` : null }); newKey.value = created.key; } editingId.value = null; createDialog.value = false; await load(); }
  catch { $q.notify({ type: "negative", message: "Could not create API key" }); }
  finally { saving.value = false; }
}
function revoke(key: ApiKey) { $q.dialog({ title: "Revoke API key?", message: `Automations using “${key.name}” will stop working.`, cancel: true, ok: { label: "Revoke", color: "negative" } }).onOk(async () => { try { await apiKeyApi.revoke(key.id); await load(); } catch { $q.notify({ type: "negative", message: "Could not revoke API key" }); } }); }
async function copy(value: string) { try { await navigator.clipboard.writeText(value); $q.notify({ type: "positive", message: "Copied to clipboard" }); } catch { $q.notify({ type: "warning", message: "Copy failed — select the text manually" }); } }
onMounted(load);
</script>

<style lang="scss" scoped>
.settings-page { max-width: 1100px; margin: 0 auto; padding: 28px 24px; }
.settings-header h1 { margin: 4px 0; color: #102a43; font-size: 28px; }
.settings-header p, .card-copy { color: #627d98; font-size: 14px; line-height: 1.55; }
.eyebrow, .doc-label { color: #1f6f8b; font-size: 11px; font-weight: 800; letter-spacing: .8px; text-transform: uppercase; }
.settings-tabs { margin-top: 24px; border-bottom: 1px solid #dce6eb; }
.settings-panels { background: transparent; }
.panel-card { margin-top: 18px; padding: 20px; border: 1px solid #dce6eb; border-radius: 14px; background: #fff; box-shadow: 0 2px 8px rgba(16,42,67,.05); }
.intro-card { display: flex; align-items: center; gap: 14px; }
.intro-icon { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 12px; color: #1f6f8b; background: #e8f4f7; }
.card-title { color: #102a43; font-size: 17px; font-weight: 750; }
.reveal-card { border-color: #86d4b5; background: #f2fbf7; }
.reveal-heading { display: flex; align-items: center; gap: 8px; color: #166534; font-weight: 750; }
.key-reveal, .code-line { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin: 12px 0; padding: 12px; border-radius: 8px; background: #102a43; color: #fff; overflow-x: auto; }
code { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }
.prefix { color: #1f6f8b; }
.doc-block { margin-top: 22px; }
pre { margin: 8px 0; padding: 14px; border-radius: 8px; background: #102a43; color: #d9f1f7; white-space: pre-wrap; overflow-x: auto; }
.docs-note { margin-top: 22px; background: #eef7fa; color: #334e68; }
.key-dialog { width: min(460px, 94vw); }
@media (max-width: 600px) { .settings-page { padding: 20px 16px; } .intro-card { align-items: flex-start; flex-wrap: wrap; } .intro-card .q-space { display: none; } .intro-card .q-btn { width: 100%; } .panel-card { padding: 16px; } }
</style>
