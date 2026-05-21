"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

export default function OnboardingPage() {
  const [employees, setEmployees] =
    useState([])

  const [selectedEmployee, setSelectedEmployee] =
    useState<any>(null)

  const [tasks, setTasks] =
    useState<any[]>([])

  const [name, setName] =
    useState("")

  const [email, setEmail] =
    useState("")

  const [role, setRole] =
    useState("Software Engineer")

  const [search, setSearch] =
  useState("")

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
  // CREATE EMPLOYEE
  // =========================

  const createEmployee = async () => {
    if (!name || !email) {
      alert("Fill all fields")

      return
    }

    try {
      await api.post(
        "/onboarding/employee",
        {
          name,
          email,
          role
        }
      )

      setName("")

      setEmail("")

      fetchEmployees()

      alert(
        "Onboarding workflow created"
      )
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // FETCH TASKS
  // =========================

  const fetchTasks = async (
    employee: any
  ) => {
    try {
      setSelectedEmployee(employee)

      const response = await api.get(
        `/onboarding/employee/${employee.id}/tasks`
      )

      setTasks(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // COMPLETE TASK
  // =========================

  const completeTask = async (
    taskId: number
  ) => {
    try {
      await api.patch(
        `/onboarding/task/${taskId}/complete`
      )

      fetchTasks(selectedEmployee)

      fetchEmployees()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="space-y-6">
      {/* HEADER */}

      <div className="rounded-3xl bg-gradient-to-r from-cyan-500/20 to-blue-500/10 p-8">
        <h1 className="text-4xl font-bold">
          Onboarding Intelligence
        </h1>

        <p className="mt-3 text-gray-300">
          AI-powered onboarding
          operations and workforce
          readiness monitoring
        </p>
      </div>

      {/* CREATE */}

      

      <div className="rounded-3xl border border-white/10 bg-[#111827] p-6">
  <div className="flex items-center justify-between">
    <div>
      <h2 className="text-2xl font-semibold">
        Employee Directory
      </h2>

      <p className="mt-2 text-gray-400">
        Search and monitor workforce onboarding
      </p>
    </div>

    <input
      type="text"
      placeholder="Search employees..."
      value={search}
      onChange={(e) =>
        setSearch(e.target.value)
      }
      className="w-[300px] rounded-2xl border border-white/10 bg-[#1F2937] p-4 outline-none"
    />
  </div>
</div>

      {/* EMPLOYEES */}

      <div className="grid gap-5 lg:grid-cols-2">
        {employees
  .filter((employee: any) =>
    employee.name
      .toLowerCase()
      .includes(
        search.toLowerCase()
      )
  )
  .map(
          (employee: any) => (
            <div
              key={employee.id}
              className="rounded-3xl border border-white/10 bg-[#111827] p-6"
            >
              {/* TOP */}

              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-semibold">
                    {employee.name}
                  </h2>

                  <p className="mt-2 text-gray-400">
                    {employee.role}
                  </p>
                </div>

                {/* STATUS */}

                <span
                  className={`rounded-full px-4 py-2 text-sm ${
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
              </div>

              {/* PROGRESS */}

              <div className="mt-6">
                <div className="mb-3 flex items-center justify-between">
                  <p className="text-sm text-gray-400">
                    Workforce Readiness
                  </p>

                  <p className="font-semibold text-cyan-300">
                    {employee.progress}%
                  </p>
                </div>

                <div className="h-4 overflow-hidden rounded-full bg-white/10">
                  <div
                    className={`h-full rounded-full ${
                      employee.progress >= 100
                        ? "bg-green-400"

                        : employee.progress >= 70
                        ? "bg-blue-400"

                        : employee.progress >= 30
                        ? "bg-yellow-400"

                        : "bg-red-400"
                    }`}
                    style={{
                      width: `${employee.progress}%`
                    }}
                  />
                </div>
              </div>

              {/* STATS */}

              <div className="mt-6 grid grid-cols-2 gap-4">
                <div className="rounded-2xl bg-black/20 p-4">
                  <p className="text-xs text-gray-400">
                    Tasks Completed
                  </p>

                  <p className="mt-2 text-xl font-semibold">
                    {
                      employee.completed_tasks
                    }
                    /
                    {
                      employee.total_tasks
                    }
                  </p>
                </div>

                <div className="rounded-2xl bg-black/20 p-4">
                  <p className="text-xs text-gray-400">
                    Pending Tasks
                  </p>

                  <p className="mt-2 text-xl font-semibold text-yellow-300">
                    {
                      employee.total_tasks -
                      employee.completed_tasks
                    }
                  </p>
                </div>
              </div>

              {/* PENDING */}

              {employee.pending_tasks
                .length > 0 && (
                <div className="mt-6 rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-5">
                  <p className="text-sm font-semibold text-yellow-300">
                    Pending Operational
                    Tasks
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {employee.pending_tasks.map(
                      (
                        task: string,
                        index: number
                      ) => (
                        <span
                          key={index}
                          className="rounded-full bg-black/20 px-3 py-2 text-xs"
                        >
                          {task}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* AI MESSAGE */}

              <div className="mt-6 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-5">
                <p className="text-sm text-gray-300">
                  {employee.progress >=
                  100
                    ? "Employee fully onboarded and operationally ready."

                    : employee.progress >=
                      70
                    ? "Employee nearing operational readiness. Minor onboarding tasks pending."

                    : employee.progress >=
                      30
                    ? "Employee onboarding in progress. Operational setup partially completed."

                    : "Employee onboarding at risk. Multiple critical tasks still pending."}
                </p>
              </div>

              {/* ACTION */}

              <div className="mt-6 flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-400">
                    Employee Email
                  </p>

                  <p className="mt-2 text-sm">
                    {employee.email}
                  </p>
                </div>

                <button
                  onClick={() =>
                    fetchTasks(employee)
                  }
                  className="rounded-2xl border border-white/10 px-5 py-3 text-sm transition hover:bg-white/5"
                >
                  View Tasks
                </button>
              </div>
            </div>
          )
        )}
      </div>

      {/* TASK MODAL */}

      {selectedEmployee && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="max-h-[80vh] w-[750px] overflow-y-auto rounded-3xl bg-[#111827] p-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold">
                  Onboarding Tasks
                </h2>

                <p className="mt-2 text-gray-400">
                  {
                    selectedEmployee.name
                  }
                </p>
              </div>

              <button
                onClick={() =>
                  setSelectedEmployee(
                    null
                  )
                }
                className="text-2xl"
              >
                ×
              </button>
            </div>

            {/* TASKS */}

            <div className="mt-8 space-y-5">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className={`rounded-2xl border p-5 ${
                    task.completed
                      ? "border-green-500/20 bg-green-500/5"
                      : "border-yellow-500/20 bg-yellow-500/5"
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-xl font-semibold">
                        {task.title}
                      </h3>

                      <p className="mt-2 text-gray-400">
                        {
                          task.description
                        }
                      </p>

                      <p className="mt-3 text-sm text-cyan-300">
                        Assigned Team:
                        {" "}
                        {
                          task.assigned_team
                        }
                      </p>
                    </div>

                    {task.completed ? (
                      <span className="rounded-full bg-green-500/20 px-4 py-2 text-sm text-green-300">
                        Completed
                      </span>
                    ) : (
                      <button
                        onClick={() =>
                          completeTask(
                            task.id
                          )
                        }
                        className="rounded-2xl bg-cyan-500 px-5 py-3 font-semibold text-black"
                      >
                        Complete
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}