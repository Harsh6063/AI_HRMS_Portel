"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

export default function AlertsPage() {
  const [alerts, setAlerts] =
    useState([])

  useEffect(() => {
  fetchAlerts()

  const interval =
    setInterval(() => {
      fetchAlerts()
    }, 5000)

  return () =>
    clearInterval(interval)
}, [])

  const fetchAlerts = async () => {
    try {
      const response = await api.get(
        "/alerts"
      )

      setAlerts(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // RESOLVE
  // =========================

  const resolveAlert = async (
    id: number
  ) => {
    try {
      await api.patch(
        `/alerts/${id}/resolve`
      )

      fetchAlerts()
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // DELETE
  // =========================

  const deleteAlert = async (
    id: number
  ) => {
    try {
      await api.delete(
        `/alerts/${id}`
      )

      fetchAlerts()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="space-y-6">
      {/* HEADER */}

      <div className="rounded-3xl bg-[#111827] p-8">
        <h1 className="text-4xl font-bold">
          Alert Center
        </h1>

        <p className="mt-2 text-gray-400">
          Real-time operational
          intelligence monitoring
        </p>
      </div>

      {/* ALERTS */}

      <div className="space-y-5">
        {alerts.map((alert: any) => (
          <div
            key={alert.id}
            className={`rounded-3xl border p-6 ${
              alert.resolved
                ? "border-green-500/20 bg-green-500/5"
                : "border-red-500/20 bg-red-500/5"
            }`}
          >
            <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
              {/* LEFT */}

              <div>
                <div className="flex items-center gap-3">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      alert.resolved
                        ? "bg-green-500/20 text-green-300"
                        : "bg-red-500/20 text-red-300"
                    }`}
                  >
                    {alert.severity}
                  </span>

                  {alert.resolved && (
                    <span className="text-sm text-green-400">
                      Resolved
                    </span>
                  )}
                </div>

                <h2 className="mt-4 text-2xl font-semibold">
                  {alert.title}
                </h2>

                <p className="mt-2 text-gray-300">
                  {alert.message}
                </p>

                <p className="mt-3 text-xs text-gray-500">
                  {new Date(
                    alert.created_at
                  ).toLocaleString()}
                </p>
              </div>

              {/* ACTIONS */}

              <div className="flex gap-3">
                {!alert.resolved && (
                  <button
                    onClick={() =>
                      resolveAlert(
                        alert.id
                      )
                    }
                    className="rounded-2xl bg-green-500 px-5 py-3 font-semibold text-black"
                  >
                    Resolve
                  </button>
                )}

                <button
                  onClick={() =>
                    deleteAlert(
                      alert.id
                    )
                  }
                  className="rounded-2xl bg-red-500 px-5 py-3 font-semibold text-white"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}