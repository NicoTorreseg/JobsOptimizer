import { Job } from "@/types/job";
import { ExternalLink, MapPin, Building2, Calendar } from "lucide-react";
import Link from "next/link";

interface JobCardProps {
    job: Job;
}

export function JobCard({ job }: JobCardProps) {
    // Format date if possible
    const date = new Date(job.created_at).toLocaleDateString("es-AR", {
        day: "numeric",
        month: "short",
    });

    return (
        <div className="group relative border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all bg-white hover:border-blue-500/50">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {job.title}
                    </h3>
                    <div className="flex items-center text-gray-600 mt-1 space-x-2 text-sm">
                        <Building2 size={16} />
                        <span className="font-medium">{job.company_name}</span>
                    </div>
                </div>
                <div className="text-xs font-semibold px-2 py-1 bg-blue-50 text-blue-700 rounded-md">
                    {job.seniority}
                </div>
            </div>

            <div className="flex items-center text-gray-500 text-sm mb-4 space-x-4">
                <div className="flex items-center space-x-1">
                    <MapPin size={14} />
                    <span>{job.location || "Remoto"}</span>
                </div>
                <div className="flex items-center space-x-1">
                    <Calendar size={14} />
                    <span>{date}</span>
                </div>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
                {job.tech_stack.map((tech) => (
                    <span
                        key={tech}
                        className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded-full border border-gray-200"
                    >
                        {tech}
                    </span>
                ))}
            </div>

            <Link
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
            >
                Ver Oferta <ExternalLink size={14} className="ml-1" />
            </Link>
        </div>
    );
}
