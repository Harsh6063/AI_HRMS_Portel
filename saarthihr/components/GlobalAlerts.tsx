"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

import { useRouter } from "next/navigation"

export default function GlobalAlerts() {
  const [alerts, setAlerts] = useState([])

  const router = useRouter()

  useEffect(() => {
    fetchAlerts()

    const interval = setInterval(() => {
      fetchAlerts()
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const fetchAlerts = async () => {
    try {
      const response = await api.get(
        "/alerts"
      )

      const activeAlerts =
        response.data.filter(
          (alert: any) =>
            !alert.resolved
        )

      setAlerts(activeAlerts)
    } catch (error) {
      console.error(error)
    }
  }

  if (alerts.length === 0) {
    return null
  }

  return (
    <div className="fixed right-5 top-5 z-50 space-y-3">
      {alerts.slice(0, 3).map((alert: any) => (
        <div
          key={alert.id}
          onClick={() =>
            router.push("/alerts")
          }
          className="w-[340px] cursor-pointer rounded-2xl border border-red-500/20 bg-[#111827] p-4 shadow-2xl transition hover:scale-[1.02]"
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-semibold text-red-400">
                {alert.severity} ALERT
              </p>

              <h2 className="mt-1 text-sm font-semibold text-white">
                {alert.title}
              </h2>

              <p className="mt-2 text-xs text-gray-400">
                {alert.message}
              </p>
            </div>

            <div className="ml-3 h-3 w-3 rounded-full bg-red-500 animate-pulse" />
          </div>
        </div>
      ))}
    </div>
  )
}