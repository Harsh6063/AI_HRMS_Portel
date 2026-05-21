import Link from "next/link"
import {
  LayoutDashboard,
  Users,
  UserPlus,
  AlertTriangle,
} from "lucide-react"

const items = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Recruitment",
    href: "/recruitment",
    icon: Users,
  },
  {
    title: "Onboarding",
    href: "/onboarding",
    icon: UserPlus,
  },
  {
    title: "Alerts",
    href: "/alerts",
    icon: AlertTriangle,
  },
  {
    title: "Employees",
    href: "/employees",
    icon: Users,
  }
]

export default function Sidebar() {
  return (
    <div className="hidden w-64 border-r border-white/10 bg-[#111827] p-6 lg:block">
      <h1 className="text-3xl font-bold text-teal-400">
        HRMS Portal
      </h1>

      <p className="mt-2 text-sm text-gray-400">
        HR Intelligence OS
      </p>

      <div className="mt-10 space-y-3">
        {items.map((item) => (
          <Link
            key={item.title}
            href={item.href}
            className="flex items-center gap-3 rounded-xl px-4 py-3 transition hover:bg-white/5"
          >
            <item.icon className="h-5 w-5 text-teal-400" />

            <span>{item.title}</span>
          </Link>
        ))}
      </div>
    </div>
  )
}