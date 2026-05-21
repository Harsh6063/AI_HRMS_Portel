"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

export default function EmployeesPage() {
  const [employees, setEmployees] =
    useState([])

  const [search, setSearch] =
    useState("")
   const deleteEmployee = async (
  id: number
) => {
  try {
    await api.delete(
      `/onboarding/employee/${id}`
    )

    fetchEmployees()
  } catch (error) {
    console.error(error)
  }
}
  // =========================
  // FETCH EMPLOYEES
  // =========================

  useEffect(() => {
    fetchEmployees()
  }, [])

  const fetchEmployees = async () => {
    try {
      const response = await api.get(
        "/onboarding/employees"
      )

      setEmployees(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // START ONBOARDING
  // =========================

  const startOnboarding = async (
    employee: any
  ) => {
    try {
      await api.post(
        `/onboarding/start/${employee.id}`
      )

      fetchEmployees()

      alert(
        "Onboarding started"
      )
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="space-y-6">
      {/* HEADER */}

      <div className="rounded-3xl bg-gradient-to-r from-purple-500/20 to-blue-500/10 p-8">
        <h1 className="text-4xl font-bold">
          Workforce Directory
        </h1>

        <p className="mt-3 text-gray-300">
          Employee onboarding and
          workforce readiness
          management
        </p>
      </div>

      {/* SEARCH */}

      <div className="rounded-3xl border border-white/10 bg-[#111827] p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">
              Employee Directory
            </h2>

            <p className="mt-2 text-gray-400">
              Search and manage
              employees
            </p>
          </div>

          <input
            type="text"
            placeholder="Search employees..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
            className="w-[320px] rounded-2xl border border-white/10 bg-[#1F2937] p-4 outline-none"
          />
        </div>
      </div>

      {/* EMPLOYEE TABLE */}

      <div className="overflow-hidden rounded-3xl border border-white/10 bg-[#111827]">
        <table className="w-full">
          <thead className="border-b border-white/10 bg-black/20">
            <tr>
              <th className="px-6 py-5 text-left text-sm text-gray-400">
                Employee
              </th>

              <th className="px-6 py-5 text-left text-sm text-gray-400">
                Role
              </th>

              <th className="px-6 py-5 text-left text-sm text-gray-400">
                Status
              </th>

              <th className="px-6 py-5 text-left text-sm text-gray-400">
                Readiness
              </th>

              <th className="px-6 py-5 text-left text-sm text-gray-400">
                Action
              </th>
            </tr>
          </thead>

          <tbody>
            {employees
              .filter((employee: any) =>
                employee.name
                  .toLowerCase()
                  .includes(
                    search.toLowerCase()
                  )
              )
              .map((employee: any) => (
                <tr
                  key={employee.id}
                  className="border-b border-white/5"
                >
                  <td className="px-6 py-5">
                    <div>
                      <h3 className="font-semibold">
                        {
                          employee.name
                        }
                      </h3>

                      <p className="mt-1 text-sm text-gray-400">
                        {
                          employee.email
                        }
                      </p>
                    </div>
                  </td>

                  <td className="px-6 py-5 text-sm">
                    {employee.role}
                  </td>

                  <td className="px-6 py-5">
                    <span
                      className={`rounded-full px-4 py-2 text-xs ${
                        employee.onboarding_status ===
                        "Fully Onboarded"
                          ? "bg-green-500/20 text-green-300"

                          : employee.onboarding_status ===
                            "Near Ready"
                          ? "bg-blue-500/20 text-blue-300"

                          : employee.onboarding_status ===
                            "In Progress"
                          ? "bg-yellow-500/20 text-yellow-300"

                          : "bg-red-500/20 text-red-300"
                      }`}
                    >
                      {
                        employee.onboarding_status
                      }
                    </span>
                  </td>

                  <td className="px-6 py-5">
                    <div className="w-[180px]">
                      <div className="mb-2 flex items-center justify-between">
                        <p className="text-xs text-gray-400">
                          {
                            employee.progress
                          }
                          %
                        </p>
                      </div>

                      <div className="h-3 overflow-hidden rounded-full bg-white/10">
                        <div
                          className={`h-full rounded-full ${
                            employee.progress >=
                            100
                              ? "bg-green-400"

                              : employee.progress >=
                                70
                              ? "bg-blue-400"

                              : employee.progress >=
                                30
                              ? "bg-yellow-400"

                              : "bg-red-400"
                          }`}
                          style={{
                            width: `${employee.progress}%`
                          }}
                        />
                      </div>
                    </div>
                  </td>

                  <td className="px-6 py-5">
  <div className="flex items-center gap-3">
    <button
      onClick={() =>
        startOnboarding(employee)
      }
      className="rounded-2xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-black transition hover:scale-[1.02]"
    >
      Start Onboarding
    </button>

    <button
      onClick={() =>
        deleteEmployee(employee.id)
      }
      className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300 transition hover:bg-red-500/20"
    >
      Remove
    </button>
  </div>
</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}