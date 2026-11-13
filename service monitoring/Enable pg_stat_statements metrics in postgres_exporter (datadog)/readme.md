# Learnings – PostgreSQL Monitoring with Datadog

## 1. What I Worked On

In this task, I set up PostgreSQL Database Monitoring using Datadog on an AWS EC2 instance.

I used Docker to run PostgreSQL and configured the Datadog Agent to collect database metrics and query information.

I also explored the Datadog dashboard to see how PostgreSQL was performing.

## 2. What I Learned

- How to run PostgreSQL using Docker.
- How to enable `pg_stat_statements` to track SQL queries.
- How to install and configure the Datadog Agent.
- How to connect Datadog with PostgreSQL.
- How to create a separate monitoring user with the required permissions.
- How to check database activity and query performance.
- How to view PostgreSQL metrics in the Datadog dashboard.
- How to use AWS Systems Manager to access the EC2 instance.
- How to generate some test queries and check whether Datadog collects them.

## 3. Pros (Advantages)

- Easy to monitor PostgreSQL from one dashboard.
- Helps identify slow and frequently running queries.
- Makes it easier to understand database performance.
- Shows active connections and query activity.
- Helps find database issues early.
- Can monitor multiple database instances.
- The separate monitoring user provides better access control.

## 4. Cons (Disadvantages)

- Datadog monitoring may increase the overall cost.
- The Datadog Agent uses some CPU and memory.
- Initial setup requires several configuration steps.
- Proper database permissions are needed.
- Internet connectivity is required to send data to Datadog.
- Query samples may contain sensitive information, so they need to be handled carefully.

## 5. Challenges I Faced

- Configuring PostgreSQL settings for monitoring.
- Enabling the `pg_stat_statements` extension.
- Setting up the Datadog monitoring user and permissions.
- Configuring the Datadog Agent.
- Fixing some Agent permission and service-related issues.
- Checking whether PostgreSQL data was reaching Datadog.
- Understanding the query metrics shown in the dashboard.

## 6. Final Result

I successfully connected PostgreSQL with Datadog Database Monitoring.

I was able to see database metrics, query information, active connections, and database activity in the Datadog dashboard.

This task helped me understand how database monitoring works and how Datadog can be used to check PostgreSQL performance.