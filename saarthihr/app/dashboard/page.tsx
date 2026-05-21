"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

export default function DashboardPage() {
  const [data, setData] =
    useState<any>(null)

  // =========================
  // FETCH DASHBOARD
  // =========================

 useEffect(() => {
  fetchDashboard()

  const interval =
    setInterval(() => {
      fetchDashboard()
    }, 5000)

  return () =>
    clearInterval(interval)
}, [])
  const fetchDashboard = async () => {
    try {
      const response = await api.get(
        "/dashboard/summary"
      )

      setData(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  if (!data) {
    return (
      <div className="p-10">
        Loading dashboard...
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* HEADER */}

      <div className="rounded-3xl bg-gradient-to-r from-teal-500/20 to-cyan-500/10 p-8">
        <h1 className="text-4xl font-bold">
          SaarthiHR Command Center
        </h1>

        <p className="mt-3 text-gray-300">
          Operational workforce
          intelligence dashboard
        </p>
      </div>

      {/* MORNING BRIEF */}

      <div className="rounded-3xl border border-cyan-500/20 bg-cyan-500/5 p-8">
        <h2 className="text-2xl font-semibold">
          Morning Brief
        </h2>

        <div className="mt-6 space-y-3 text-gray-300">
          <p>
            • {data.total_candidates}
            {" "}candidates in pipeline
          </p>

          <p>
            • {data.high_ats}
            {" "}high ATS candidates
          </p>

          <p>
            • {data.interviews}
            {" "}interviews in progress
          </p>

          <p>
            • {data.onboarding_started}
            {" "}employees onboarding
          </p>

          <p>
            • Workforce readiness:
            {" "}
            {data.avg_readiness}%
          </p>

          <p>
            • {data.total_alerts}
            {" "}active operational alerts
          </p>
        </div>
      </div>

      <div className="rounded-3xl border border-cyan-500/20 bg-cyan-500/5 p-8">
  <h2 className="text-2xl font-semibold">
    AI Operational Insights
  </h2>

  <div className="mt-6 space-y-4">
    {data.insights.map(
      (
        insight: string,
        index: number
      ) => (
        <div
          key={index}
          className="rounded-2xl bg-black/20 p-5"
        >
          <p className="text-gray-300">
            {insight}
          </p>
        </div>
      )
    )}
  </div>
</div>

      {/* METRICS */}

      <div className="grid gap-5 md:grid-cols-3 xl:grid-cols-4">
        <MetricCard
          title="Candidates Applied"
          value={
            data.total_candidates
          }
        />

        <MetricCard
          title="High ATS"
          value={data.high_ats}
        />

        <MetricCard
          title="Interviews"
          value={data.interviews}
        />

        <MetricCard
          title="Offers"
          value={data.offers}
        />

        <MetricCard
          title="Hired"
          value={data.hired}
        />

        <MetricCard
          title="Onboarding Started"
          value={
            data.onboarding_started
          }
        />

        <MetricCard
          title="Fully Onboarded"
          value={
            data.fully_onboarded
          }
        />

        <MetricCard
          title="Pending Onboarding"
          value={
            data.pending_onboarding
          }
        />
      </div>

      {/* READINESS */}

      <div className="rounded-3xl border border-white/10 bg-[#111827] p-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">
              Workforce Readiness
            </h2>

            <p className="mt-2 text-gray-400">
              Organization operational
              readiness score
            </p>
          </div>

          <div className="text-5xl font-bold text-cyan-300">
            {data.avg_readiness}%
          </div>
        </div>

        <div className="mt-8 h-5 overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-cyan-400"
            style={{
              width: `${data.avg_readiness}%`
            }}
          />
        </div>
      </div>

      <div className="rounded-3xl border border-white/10 bg-[#111827] p-8">
  <h2 className="text-2xl font-semibold">
    Operational Timeline
  </h2>

  <div className="mt-8 space-y-4">
    {data.timeline.map(
      (
        item: any,
        index: number
      ) => (
        <div
          key={index}
          className="rounded-2xl border border-white/5 bg-black/20 p-5"
        >
          <h3 className="font-semibold text-cyan-300">
            {item.event}
          </h3>

          <p className="mt-2 text-gray-400">
            {item.description}
          </p>
        </div>
      )
    )}
  </div>
</div>

      {/* ALERTS */}

      <div className="rounded-3xl border border-red-500/20 bg-[#111827] p-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">
              Operational Alerts
            </h2>

            <p className="mt-2 text-gray-400">
              Real-time workflow risks
              and escalations
            </p>
          </div>

          <div className="rounded-full bg-red-500/20 px-5 py-3 text-sm text-red-300">
            {data.total_alerts}
            {" "}Active Alerts
          </div>
        </div>

        <div className="mt-8 space-y-4">
          {data.alerts.map(
            (alert: any) => (
              <div
                key={alert.id}
                className="rounded-2xl border border-red-500/10 bg-red-500/5 p-5"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-red-300">
                    {alert.title}
                  </h3>

                  <span className="rounded-full bg-red-500/20 px-3 py-1 text-xs">
                    {
                      alert.severity
                    }
                  </span>
                </div>

                <p className="mt-3 text-gray-300">
                  {alert.message}
                </p>

                <div className="rounded-3xl border border-yellow-500/20 bg-[#111827] p-8">
  <h2 className="text-2xl font-semibold">
    SLA Monitoring
  </h2>

  <p className="mt-2 text-gray-400">
    Workflow bottlenecks and delayed operations
  </p>

  <div className="mt-8 space-y-4">
    {data.sla_issues.map(
      (
        issue: any,
        index: number
      ) => (
        <div
          key={index}
          className="rounded-2xl border border-yellow-500/10 bg-yellow-500/5 p-5"
        >
          <h3 className="font-semibold text-yellow-300">
            {issue.title}
          </h3>

          <p className="mt-2 text-gray-300">
            {issue.message}
          </p>
        </div>
      )
    )}
  </div>
</div>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  )
}



// =========================
// METRIC CARD
// =========================

function MetricCard({
  title,
  value
}: any) {
  return (
    <div className="rounded-3xl border border-white/10 bg-[#111827] p-6">
      <p className="text-sm text-gray-400">
        {title}
      </p>

      <h2 className="mt-4 text-4xl font-bold">
        {value}
      </h2>
    </div>
  )
}