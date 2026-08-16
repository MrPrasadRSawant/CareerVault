import type { OpportunityStatus } from "@/api/opportunities";
import {
  OPPORTUNITY_STATUS_LABELS,
  OPPORTUNITY_STATUS_ORDER
} from "@/modules/shared/statusColors";
import type { OpportunityExportColumn, OpportunityFilters } from "./types";

export const opportunityStatusOptions = OPPORTUNITY_STATUS_ORDER.map(value => ({
  label: OPPORTUNITY_STATUS_LABELS[value],
  value
}));

export function createDefaultFilters(): OpportunityFilters {
  return {
    search: "",
    statuses: [],
    company: "",
    location: "",
    experience: "",
    skills: "",
    postedFrom: "",
    postedTo: ""
  };
}

export function formatOpportunityDate(
  value: string | null | undefined
): string {
  return value ? new Date(value).toLocaleDateString() : "—";
}

export function statusLabel(status: OpportunityStatus): string {
  return OPPORTUNITY_STATUS_LABELS[status];
}

export function normalizeDateTime(value: string): string | null {
  if (!value) return null;
  return value.length === 16 ? `${value}:00Z` : value;
}

export function toLocalDateTime(value: string | null): string {
  if (!value) return "";
  const date = new Date(value);
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];
    if (char === '"' && quoted && next === '"') {
      cell += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(cell.trim());
      cell = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") index += 1;
      row.push(cell.trim());
      if (row.some(Boolean)) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  if (cell || row.length) {
    row.push(cell.trim());
    rows.push(row);
  }
  return rows;
}

const exportValue = (value: unknown): string => {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.join(", ");
  if (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  ) {
    return `${value}`;
  }
  return JSON.stringify(value);
};

export const opportunityExportColumns: OpportunityExportColumn[] = [
  { key: "title", label: "Role", value: opportunity => opportunity.title },
  {
    key: "company_name",
    label: "Company",
    value: opportunity => exportValue(opportunity.company_name)
  },
  {
    key: "status",
    label: "Status",
    value: opportunity => statusLabel(opportunity.status)
  },
  {
    key: "job_location",
    label: "Location",
    value: opportunity => exportValue(opportunity.job_location)
  },
  {
    key: "post_url",
    label: "Job post URL",
    value: opportunity => exportValue(opportunity.post_url)
  },
  {
    key: "company_career_page",
    label: "Career page URL",
    value: opportunity => exportValue(opportunity.company_career_page)
  },
  {
    key: "company_url",
    label: "Company URL",
    value: opportunity => exportValue(opportunity.company_url)
  },
  {
    key: "posted_on_utc",
    label: "Posted (UTC)",
    value: opportunity => exportValue(opportunity.posted_on_utc)
  },
  {
    key: "experience_level",
    label: "Experience",
    value: opportunity => exportValue(opportunity.experience_level)
  },
  {
    key: "required_skills",
    label: "Skills",
    value: opportunity => exportValue(opportunity.required_skills)
  },
  {
    key: "description",
    label: "Description",
    value: opportunity => exportValue(opportunity.description)
  },
  {
    key: "created_on_utc",
    label: "Created (UTC)",
    value: opportunity => opportunity.created_on_utc
  },
  {
    key: "updated_on_utc",
    label: "Updated (UTC)",
    value: opportunity => opportunity.updated_on_utc
  }
];

export function csvEscape(value: string): string {
  return /[",\n\r]/.test(value) ? `"${value.replace(/"/g, '""')}"` : value;
}
