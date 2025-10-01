📘 **FieldAI Web Application**

## 1. Overview

**Project**: FieldAI Management System

**Tech Stack**:

- **Backend**: Django 5.2.5 (Python 3.12)  
- **Database**: PostgreSQL (Supabase hosted)  
- **Frontend**: Django Templates + Bootstrap 5 + FontAwesome  
- **Deployment**: Dockerized, hosted on Blade server (with Supabase DB connection)  
- **Auth**: CustomUser model with role-based access  
  - Roles: Admin, Manager, Engineer, Client, Accounts, PMO

**Key Modules**:

1. Accounts & Authentication  
2. Dashboard (role-specific)  
3. Job Management  
4. Timesheet Management  
5. Invoices  
6. Notifications & Real-time Updates  
7. Reports  
8. Skills Management (PMO)  
9. Admin Panel (Jazzmin Theme)  

---

## 2. Accounts & Authentication

- **Purpose**: Handle user login, registration, roles, and permissions.

- **Roles**:
  - `admin`: Full control  
  - `manager`: Oversee jobs, engineers, reports  
  - `engineer`: Work on assigned jobs, log timesheets  
  - `client`: Create and track jobs  
  - `accounts`: Manage invoices  
  - `PMO`: Supervisory role (read-only with warnings on modifications)

- **Files**:
  - `accounts/models.py` → CustomUser model with role field  
  - `accounts/forms.py` → Login/Profile forms  
  - `accounts/views.py` → Login/logout, profile management  
  - `accounts/admin.py` → Custom admin configuration  
  - `accounts/urls.py` → `/accounts/login`, `/accounts/logout`, `/accounts/profile`

- **Notes**:
  - PMO restrictions enforced via middleware: `core/middleware.py`  
  - Group-based permissions configured with `management command`: `create_pmo_group.py`

---

## 3. Dashboard (Role-based)

- **Purpose**: Provide tailored view depending on user role.

- **Files**:
  - `dashboard/views.py` → `admin_dashboard`, `manager_dashboard`, `engineer_dashboard`, `client_dashboard`, `accounts_dashboard`  
  - `dashboard/templates/dashboard/`  
  - `dashboard/urls.py`

- **Features**:
  - Manager: view jobs, engineers, reports, notifications  
  - Engineer: view assigned jobs, submit timesheet  
  - Client: view/create jobs  
  - Accounts: view/manage invoices

---

## 4. Job Management

- **Purpose**: Centralized system to raise, assign, and track jobs.

- **Features**:
  - Client can create jobs (auto-assigned client, no engineer assignment)  
  - PMO/Manager assigns jobs to engineers  
  - Engineers update status

- **Files**:
  - `accounts/models.py` → Job model (fields: job_id, title, description, client, engineer, status, priority, location, etc.)  
  - `accounts/forms.py` → `JobForm` (dynamic: hides engineer/client fields for clients)  
  - `dashboard/views.py` → `job_list`, `job_detail`, `job_create`  
  - `dashboard/templates/dashboard/jobs/`  
  - `dashboard/urls.py`

- **Job ID Format**: `JOB-0001` (generated in `Job.save()` override)

---

## 5. Timesheet Management

- **Purpose**: Log engineer hours against tasks/tickets; provide reporting to PMO.

- **Features**:
  - Engineers add timesheet entries (date, coverage hours, task details, minutes spent, comments)  
  - PMO/Manager view all entries  
  - Engineer view personal entries only

- **Files**:
  - `accounts/models.py` → `TimesheetEntry`  
  - `dashboard/forms.py` → `TimesheetEntryForm`  
  - `dashboard/views.py` → `add_timesheet_entry`, `view_timesheet`  
  - `dashboard/templates/dashboard/add_entry.html`, `view_entries.html`

---

## 6. Invoices

- **Purpose**: Track and manage invoices for clients.

- **Roles**:
  - Client: view invoices  
  - Accounts team: create/manage invoices

- **Files**:
  - `invoices/models.py` → `Invoice`, `InvoiceItem`  
  - `invoices/views.py` → `invoice_list`, `invoice_detail`, `invoice_create`  
  - `invoices/templates/invoices/`  
  - `invoices/urls.py`

- **Notes**:
  - Integrated with Jobs → invoices can be linked to jobs  
  - Accounts role has full access

---

## 7. Notifications & Real-time Updates

- **Purpose**: Notify relevant users on job/timesheet/invoice changes.

- **Types**:
  - Email notifications  
  - In-app notifications (for manager, accounts, PMO)

- **Files**:
  - `dashboard/views.py` → `manager_notifications`, `accounts_notifications`  
  - `dashboard/templates/dashboard/notifications.html`  
  - JS polling in `base.html` → refreshes notification badge every 30s  
  - `core/middleware.py` → PMO warnings on restricted actions

---

## 8. Reports

- **Manager Reports**: Overview of jobs, engineer activity, timesheets.  
- **Engineer Reports**: Personal timesheet and job summary.

- **Files**:
  - `dashboard/views.py` → `manager_report_view`, `engineer_report_view`  
  - `dashboard/templates/dashboard/reports/`

---

## 9. Skills Management (PMO)

- **Purpose**: PMO can define skills for engineers.

- **Model**: `Skill` with `name`, `description`, `category`.

- **Files**:
  - `accounts/models.py` → `Skill`  
  - `accounts/forms.py` → `SkillForm`  
  - `dashboard/views.py` → `skill_list`, `skill_create`  
  - `dashboard/templates/dashboard/skills/`

---

## 10. Admin Panel (dazy Theme+ zazzmin)

- **Purpose**: Provide a styled Django admin panel.

- **Config**: `settings.py` → `JAZZMIN_SETTINGS`

- **Issue**:
  - If not loading properly, ensure static files are collected:  
    ```
    python manage.py collectstatic
    ```

---

## 11. Error Handling

- **Custom Error Pages**:
  - `templates/404.html` → User-friendly error page for unknown routes

- **Settings**:
  ```python
  DEBUG = True
  ALLOWED_HOSTS = ["127.0.0.1", "210.18.187.162"]
  handler404 = "core.views.custom_404_view"
  ```

---

## 12. Deployment & DB

- **Supabase Postgres**:

  * Configured via `settings.py` → `DATABASES`
  * `DATABASE_URL` pulled from `settings.py`
  * To migrate from personal to company Supabase:

    ```bash
    # Update DATABASE_URL in settings.py
    python manage.py migrate --fake-initial
    ```

- **Docker**:

  * `Dockerfile` builds Django app

---

## 13. File Structure

 ```bash
mgmt_v2/
├── accounts/
│   ├── models.py (CustomUser, Job, TimesheetEntry, Skill)
│   ├── forms.py (LoginForm, JobForm, TimesheetEntryForm, SkillForm)
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│
├── dashboard/
│   ├── views.py (dashboards, jobs, reports, notifications, skills)
│   ├── templates/dashboard/
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── accounts_notifications.html
│   │   ├── accounts.html
│   │   ├── add_engineer.html
│   │   ├── add_entry.html
│   │   ├── add_job.html
│   │   ├── add_skill.html
│   │   ├── admin.html
│   │   ├── client_detail.html
│   │   ├── client_form.html
│   │   ├── client_jobs.html
│   │   ├── client_list.html
│   │   ├── client.html
│   │   ├── edit_engineer.html
│   │   ├── edit_job.html
│   │   ├── eng_job_detail.html
│   │   ├── engineer_detail.html
│   │   ├── engineer_job_detail.html
│   │   ├── engineer_jobs.html
│   │   ├── engineer_report.html
│   │   ├── engineer.html
│   │   ├── expense_report.html
│   │   ├── freelancer_confirm_delete.html
│   │   ├── freelancer_form.html
│   │   ├── freelancer_list.html
│   │   ├── freelancer_upload.html
│   │   ├── get_location.html
│   │   ├── home.html
│   │   ├── invoice_detail.html
│   │   ├── invoice_form.html
│   │   ├── invoice_list.html
│   │   ├── job_detail.html
│   │   ├── job_form.html
│   │   ├── log_time.html
│   │   ├── manager_engineers.html
│   │   ├── manager_job_updates_real_time.html
│   │   ├── manager_job_updates.html
│   │   ├── manager_jobs.html
│   │   ├── manager_real_time_dashboard.html
│   │   ├── manager_report.html
│   │   ├── manager.html
│   │   ├── sidebar_links.html
│   │   ├── skill_list.html
│   │   ├── t.html
│   │   ├── upload_engineer_csv.html
│   │   ├── view_entries.html
│
├── field_mgmt/
│   ├── settings.py
│   ├── urls.py
│
├── invoices/
│   ├── models.py
│   ├── views.py
│   ├── templates/invoices/
│   ├── urls.py
│
├── core/
│   ├── middleware.py (PMO restriction)
│   ├── admin_mixins.py (PMO read-only admin)
│   ├── decorators.py
│   ├── context_processors.py
│
├── junk/
├── media/
│   ├── expense_report/
│   ├── jobs_notes/
│
├── templates/
│   ├── accounts/
│   │   └── login.html
│   ├── error/
│   │   └── 404.html
│   ├── partials/
│       ├── footer.html
│       ├── header.html
│       └── sidebar.html
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
```
