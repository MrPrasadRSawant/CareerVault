<template>
  <q-page class="admin-users-page">
    <div class="page-header">
      <div>
        <div class="page-kicker">Account governance</div>
        <h1>Users</h1>
        <p>
          Review account roles, registration dates, and sign-in access. Personal
          career information is not exposed to administrators.
        </p>
      </div>
      <q-btn
        flat
        round
        icon="refresh"
        color="grey-7"
        :loading="loading"
        aria-label="Refresh users"
        @click="load"
      >
        <q-tooltip>Refresh users</q-tooltip>
      </q-btn>
    </div>

    <div class="filters-card">
      <q-input
        v-model="search"
        outlined
        dense
        clearable
        debounce="300"
        placeholder="Search account name or email"
        class="search-field"
      >
        <template #prepend><q-icon name="search" /></template>
      </q-input>
      <q-select
        v-model="roleFilter"
        outlined
        dense
        emit-value
        map-options
        clearable
        label="Role"
        :options="roleOptions"
        class="filter-field"
      />
      <q-select
        v-model="activeFilter"
        outlined
        dense
        emit-value
        map-options
        clearable
        label="Account status"
        :options="statusOptions"
        class="filter-field"
      />
      <q-btn
        v-if="search || activeFilter !== null || roleFilter !== null"
        flat
        no-caps
        icon="restart_alt"
        label="Clear"
        @click="clearFilters"
      />
      <span class="result-count">
        {{ total }} {{ total === 1 ? "user" : "users" }}
      </span>
    </div>

    <section class="table-card">
      <q-table
        flat
        :rows="users"
        :columns="columns"
        row-key="id"
        :loading="loading"
        hide-pagination
        no-data-label="No user accounts match these filters"
        @row-click="openDetails"
      >
        <template #body-cell-user="props">
          <q-td :props="props">
            <div class="user-cell">
              <UserInitialsAvatar :name="props.row.full_name" />
              <div>
                <strong>{{ props.row.full_name }}</strong>
                <span>{{ props.row.email }}</span>
              </div>
            </div>
          </q-td>
        </template>
        <template #body-cell-role="props">
          <q-td :props="props">
            <span
              class="role-chip"
              :class="{ 'role-chip--admin': props.row.role === 'system_admin' }"
            >
              <q-icon
                :name="
                  props.row.role === 'system_admin'
                    ? 'admin_panel_settings'
                    : 'person'
                "
              />
              {{ roleLabel(props.row.role) }}
            </span>
          </q-td>
        </template>
        <template #body-cell-status="props">
          <q-td :props="props">
            <span
              class="status-chip"
              :class="
                props.row.is_active
                  ? 'status-chip--active'
                  : 'status-chip--blocked'
              "
            >
              <i></i>{{ props.row.is_active ? "Active" : "Blocked" }}
            </span>
          </q-td>
        </template>
        <template #body-cell-created_at="props">
          <q-td :props="props">{{ formatDate(props.row.created_at) }}</q-td>
        </template>
        <template #body-cell-actions="props">
          <q-td :props="props" @click.stop>
            <q-btn
              v-if="isManageable(props.row)"
              flat
              round
              dense
              :icon="props.row.is_active ? 'block' : 'lock_open'"
              :color="props.row.is_active ? 'negative' : 'primary'"
              :loading="updatingIds.includes(props.row.id)"
              :aria-label="props.row.is_active ? 'Block user' : 'Unblock user'"
              @click="confirmStatusChange(props.row)"
            >
              <q-tooltip>
                {{ props.row.is_active ? "Block account" : "Unblock account" }}
              </q-tooltip>
            </q-btn>
            <q-icon
              v-else
              name="verified_user"
              color="grey-6"
              size="20px"
              aria-label="Protected administrator account"
            >
              <q-tooltip>Protected administrator account</q-tooltip>
            </q-icon>
          </q-td>
        </template>
      </q-table>

      <div v-if="!loading && total > 0" class="table-footer">
        <span>Showing {{ firstRecord }}–{{ lastRecord }} of {{ total }}</span>
        <q-pagination
          v-model="page"
          :max="pageCount"
          :max-pages="6"
          boundary-numbers
          direction-links
          color="primary"
        />
      </div>
    </section>

    <q-dialog v-model="detailsOpen">
      <q-card v-if="selectedUser" class="details-card">
        <q-card-section class="details-heading">
          <UserInitialsAvatar
            :name="selectedUser.full_name"
            size="52px"
            font-size="14px"
          />
          <div>
            <h2>{{ selectedUser.full_name }}</h2>
            <p>{{ selectedUser.email }}</p>
          </div>
          <q-space />
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>
        <q-separator />
        <q-card-section>
          <div class="account-facts">
            <div>
              <span>Assigned role</span>
              <strong>{{ roleLabel(selectedUser.role) }}</strong>
            </div>
            <div>
              <span>Account access</span>
              <strong>{{
                selectedUser.is_active ? "Active" : "Blocked"
              }}</strong>
            </div>
            <div>
              <span>Registered</span>
              <strong>{{ formatDateTime(selectedUser.created_at) }}</strong>
            </div>
            <div>
              <span>Account updated</span>
              <strong>{{ formatDateTime(selectedUser.updated_at) }}</strong>
            </div>
            <div class="account-id">
              <span>Account ID</span>
              <strong>{{ selectedUser.id }}</strong>
            </div>
          </div>
          <div class="privacy-note">
            <q-icon name="privacy_tip" />
            <span>
              This view contains account administration data only. Job
              opportunities, applications, résumés, and other career details
              remain private.
            </span>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat no-caps label="Close" v-close-popup />
          <q-btn
            flat
            no-caps
            icon="policy"
            label="Login activity"
            :to="{
              name: 'system-admin-login-activity',
              query: { search: selectedUser.email }
            }"
          />
          <q-btn
            v-if="isManageable(selectedUser)"
            unelevated
            no-caps
            :color="selectedUser.is_active ? 'negative' : 'primary'"
            :icon="selectedUser.is_active ? 'block' : 'lock_open'"
            :label="selectedUser.is_active ? 'Block user' : 'Unblock user'"
            @click="changeSelectedStatus"
          />
          <span v-else class="protected-label">
            <q-icon name="verified_user" /> Protected administrator
          </span>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import type { QTableProps } from "quasar";
import type { AdminUser } from "@/api/admin";
import type { UserRole } from "@/api/auth";
import UserInitialsAvatar from "./components/UserInitialsAvatar.vue";
import { useAdminUsers } from "./composables/useAdminUsers";

defineOptions({ name: "AdminUsersPage" });

const statusOptions = [
  { label: "Active", value: true },
  { label: "Blocked", value: false }
];
const roleOptions = [
  { label: "Job Applicant", value: "job_applicant" },
  { label: "System Admin", value: "system_admin" }
];
const columns: QTableProps["columns"] = [
  {
    name: "user",
    label: "User account",
    align: "left",
    field: "full_name",
    sortable: true
  },
  { name: "role", label: "Role", align: "left", field: "role", sortable: true },
  {
    name: "created_at",
    label: "Registered",
    align: "left",
    field: "created_at",
    sortable: true
  },
  { name: "status", label: "Access", align: "left", field: "is_active" },
  { name: "actions", label: "Action", align: "right", field: "id" }
];
const selectedUser = ref<AdminUser | null>(null);
const detailsOpen = ref(false);
const {
  users,
  total,
  loading,
  updatingIds,
  search,
  activeFilter,
  roleFilter,
  page,
  pageCount,
  load,
  clearFilters,
  confirmStatusChange
} = useAdminUsers();
const firstRecord = computed(() =>
  total.value === 0 ? 0 : (page.value - 1) * 20 + 1
);
const lastRecord = computed(() => Math.min(page.value * 20, total.value));
const roleLabel = (role: UserRole) =>
  role === "system_admin" ? "System Admin" : "Job Applicant";
const isManageable = (user: AdminUser) => user.role === "job_applicant";
const formatDate = (value: string) =>
  new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric"
  }).format(new Date(value));
const formatDateTime = (value: string) =>
  new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit"
  }).format(new Date(value));

function openDetails(_event: Event, row: AdminUser) {
  selectedUser.value = row;
  detailsOpen.value = true;
}

function changeSelectedStatus() {
  if (!selectedUser.value) return;
  confirmStatusChange(selectedUser.value);
  detailsOpen.value = false;
}

onMounted(load);
</script>

<style lang="scss" scoped>
.admin-users-page {
  max-width: 1360px;
  margin: 0 auto;
  padding: 26px 28px 42px;
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 21px;
}
.page-kicker {
  margin-bottom: 4px;
  color: #1769e0;
  font-size: 10.5px;
  font-weight: 750;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}
.page-header h1 {
  margin: 0;
  color: #172033;
  font-size: 25px;
  font-weight: 780;
  letter-spacing: -0.45px;
}
.page-header p {
  max-width: 760px;
  margin: 4px 0 0;
  color: #748094;
  font-size: 13px;
}
.filters-card {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 13px;
  padding: 12px;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
}
.search-field {
  flex: 1;
  max-width: 410px;
}
.filter-field {
  width: 180px;
}
.result-count {
  margin-left: auto;
  color: #8a95a5;
  font-size: 11.5px;
}
.table-card {
  overflow: hidden;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}
.table-card :deep(tbody tr) {
  cursor: pointer;
}
.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 220px;
}
.user-cell strong,
.user-cell span {
  display: block;
}
.user-cell strong {
  color: #354154;
  font-size: 12.5px;
}
.user-cell span {
  margin-top: 2px;
  color: #8a95a5;
  font-size: 10.5px;
}
.role-chip,
.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 9.5px;
  font-weight: 700;
}
.role-chip {
  color: #416b9f;
  background: #edf4ff;
}
.role-chip--admin {
  color: #6256bf;
  background: #f1efff;
}
.status-chip i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.status-chip--active {
  color: #287a56;
  background: #edf8f3;
}
.status-chip--active i {
  background: #2da873;
}
.status-chip--blocked {
  color: #a33f48;
  background: #fff0f1;
}
.status-chip--blocked i {
  background: #d35d66;
}
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 13px 15px;
  border-top: 1px solid #edf0f3;
  color: #8a95a5;
  font-size: 10.5px;
}
.details-card {
  width: min(560px, 94vw);
  border-radius: 14px;
}
.details-heading {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
}
.details-heading h2 {
  margin: 0;
  color: #263449;
  font-size: 17px;
  font-weight: 750;
}
.details-heading p {
  margin: 3px 0 0;
  color: #8a95a5;
  font-size: 11px;
}
.account-facts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.account-facts > div {
  padding: 12px;
  border-radius: 9px;
  background: #f6f8fb;
}
.account-facts span,
.account-facts strong {
  display: block;
}
.account-facts span {
  color: #8c97a7;
  font-size: 9.5px;
}
.account-facts strong {
  margin-top: 4px;
  color: #3d495c;
  font-size: 11px;
}
.account-facts .account-id {
  grid-column: 1 / -1;
}
.account-id strong {
  overflow-wrap: anywhere;
  font-family: monospace;
  font-weight: 600;
}
.privacy-note {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin-top: 14px;
  padding: 11px;
  border: 1px solid #dfe8f5;
  border-radius: 9px;
  color: #64748a;
  background: #f5f9ff;
  font-size: 10px;
  line-height: 1.5;
}
.privacy-note .q-icon {
  flex: 0 0 auto;
  color: #1769e0;
  font-size: 18px;
}
.protected-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 10px;
  color: #697587;
  font-size: 10.5px;
  font-weight: 650;
}

@media (max-width: 900px) {
  .filters-card {
    flex-wrap: wrap;
  }
  .result-count {
    width: 100%;
    margin-left: 0;
  }
}
@media (max-width: 760px) {
  .admin-users-page {
    padding: 20px 16px 34px;
  }
  .filters-card {
    align-items: stretch;
    flex-direction: column;
  }
  .search-field,
  .filter-field {
    width: 100%;
    max-width: none;
  }
  .page-header {
    align-items: flex-start;
  }
  .table-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
@media (max-width: 520px) {
  .account-facts {
    grid-template-columns: 1fr;
  }
  .account-facts .account-id {
    grid-column: auto;
  }
}
</style>
