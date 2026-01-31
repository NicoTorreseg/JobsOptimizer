export interface Job {
    id: number;
    title: string;
    company_name: string;
    location: string;
    url: string;
    description_raw: string;
    seniority: string;
    tech_stack: string[];
    created_at: string;
}
