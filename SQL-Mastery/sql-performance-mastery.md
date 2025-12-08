# SQL Performance Mastery - Complete Guide
## Query Optimization, Time Complexity, and Modern SQL Features

---

## Table of Contents

1. [SQL Fundamentals & Performance Basics](#1-sql-fundamentals--performance-basics)
2. [Query Optimization Techniques](#2-query-optimization-techniques)
3. [Indexing Strategies](#3-indexing-strategies)
4. [Advanced Query Patterns](#4-advanced-query-patterns)
5. [Window Functions & Modern SQL](#5-window-functions--modern-sql)
6. [CTEs and Recursive Queries](#6-ctes-and-recursive-queries)
7. [Join Optimization](#7-join-optimization)
8. [Subquery Optimization](#8-subquery-optimization)
9. [Aggregation & Grouping](#9-aggregation--grouping)
10. [Time Complexity Analysis](#10-time-complexity-analysis)
11. [Execution Plans & Profiling](#11-execution-plans--profiling)
12. [Database-Specific Optimizations](#12-database-specific-optimizations)
13. [JSON & Modern Data Types](#13-json--modern-data-types)
14. [Partitioning & Sharding](#14-partitioning--sharding)
15. [Best Practices & Anti-Patterns](#15-best-practices--anti-patterns)

---

## 1. SQL Fundamentals & Performance Basics

### Understanding Query Execution Order

SQL queries are executed in a specific order, not the order you write them:

```sql
-- Written order:
SELECT column1, column2, COUNT(*) as count
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.table1_id
WHERE t1.status = 'active'
GROUP BY column1, column2
HAVING COUNT(*) > 10
ORDER BY count DESC
LIMIT 10;

-- Actual execution order:
-- 1. FROM (including JOINs) - O(n*m) if no indexes
-- 2. WHERE - O(n) filtering
-- 3. GROUP BY - O(n log n) sorting
-- 4. HAVING - O(groups) filtering
-- 5. SELECT - O(rows) projection
-- 6. ORDER BY - O(n log n) sorting
-- 7. LIMIT - O(1) limiting
```

### Basic Performance Principles

**1. SELECT Only What You Need**
```sql
-- ❌ BAD: O(n) - fetches all columns
SELECT * FROM users WHERE id = 1;

-- ✅ GOOD: O(1) - fetches only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

**2. Use WHERE to Filter Early**
```sql
-- ❌ BAD: O(n*m) - joins all rows then filters
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- ✅ GOOD: O(n) - filters before join
SELECT u.name, o.total
FROM (SELECT * FROM users WHERE created_at > '2024-01-01') u
JOIN orders o ON u.id = o.user_id;
```

**3. Limit Result Sets**
```sql
-- ❌ BAD: O(n) - returns all rows
SELECT * FROM orders ORDER BY created_at DESC;

-- ✅ GOOD: O(k log n) - returns only top k
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
```

---

## 2. Query Optimization Techniques

### 2.1 Index Usage

**Understanding Index Types:**

```sql
-- B-Tree Index (Default) - O(log n) lookup
CREATE INDEX idx_user_email ON users(email);

-- Hash Index (Equality only) - O(1) average
CREATE INDEX idx_user_id_hash ON users USING HASH(id);

-- Composite Index - O(log n) for prefix matches
CREATE INDEX idx_user_status_created ON users(status, created_at);

-- Partial Index - Smaller, faster
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering Index - Includes all needed columns
CREATE INDEX idx_user_covering ON users(id, name, email, status);
```

**Index Selection Strategy:**

```sql
-- Query 1: Single column lookup - O(log n)
SELECT * FROM users WHERE email = 'user@example.com';
-- Use: CREATE INDEX idx_email ON users(email);

-- Query 2: Range query - O(log n + k) where k is result size
SELECT * FROM users WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
-- Use: CREATE INDEX idx_created ON users(created_at);

-- Query 3: Multiple conditions - O(log n)
SELECT * FROM users WHERE status = 'active' AND created_at > '2024-01-01';
-- Use: CREATE INDEX idx_status_created ON users(status, created_at);
-- Note: Put equality first, then range
```

### 2.2 Query Rewriting for Performance

**Example 1: IN vs EXISTS**

```sql
-- ❌ BAD: O(n*m) - may scan all orders for each user
SELECT u.id, u.name
FROM users u
WHERE u.id IN (SELECT user_id FROM orders WHERE total > 1000);

-- ✅ GOOD: O(n) - stops at first match
SELECT u.id, u.name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.user_id = u.id AND o.total > 1000
);

-- ✅ BETTER: O(n) - with proper index on (user_id, total)
SELECT DISTINCT u.id, u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 1000;
```

**Example 2: DISTINCT vs GROUP BY**

```sql
-- ❌ BAD: O(n log n) - sorts entire result
SELECT DISTINCT user_id, status FROM orders;

-- ✅ GOOD: O(n) - if index exists on (user_id, status)
SELECT user_id, status 
FROM orders 
GROUP BY user_id, status;
```

**Example 3: Subquery vs JOIN**

```sql
-- ❌ BAD: O(n*m) - correlated subquery
SELECT 
    u.id,
    u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- ✅ GOOD: O(n) - single pass with aggregation
SELECT 
    u.id,
    u.name,
    COALESCE(o.order_count, 0) as order_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

### 2.3 Avoiding Full Table Scans

```sql
-- ❌ BAD: O(n) - full table scan
SELECT * FROM users WHERE UPPER(name) = 'JOHN';

-- ✅ GOOD: O(log n) - index scan with function-based index
CREATE INDEX idx_upper_name ON users(UPPER(name));
SELECT * FROM users WHERE UPPER(name) = 'JOHN';

-- ✅ ALTERNATIVE: O(log n) - store normalized data
ALTER TABLE users ADD COLUMN name_upper VARCHAR(255);
CREATE INDEX idx_name_upper ON users(name_upper);
UPDATE users SET name_upper = UPPER(name);
SELECT * FROM users WHERE name_upper = 'JOHN';
```

---

## 3. Indexing Strategies

### 3.1 Composite Index Order

**Rule: Equality → Range → Order By**

```sql
-- Query pattern:
SELECT * FROM orders 
WHERE status = 'pending'           -- Equality
  AND created_at > '2024-01-01'   -- Range
ORDER BY total DESC;              -- Order by

-- ✅ CORRECT index order:
CREATE INDEX idx_orders_opt ON orders(status, created_at, total DESC);

-- ❌ WRONG - range before equality:
CREATE INDEX idx_orders_bad ON orders(created_at, status, total);
```

### 3.2 Covering Indexes

```sql
-- Query:
SELECT id, name, email, status 
FROM users 
WHERE status = 'active';

-- ❌ Without covering index: O(log n + k) - index lookup + table access
CREATE INDEX idx_status ON users(status);
-- Still needs to access table for name, email

-- ✅ With covering index: O(log n) - index only scan
CREATE INDEX idx_status_covering ON users(status) INCLUDE (id, name, email);
-- PostgreSQL syntax
-- OR
CREATE INDEX idx_status_covering ON users(status, id, name, email);
-- MySQL syntax - includes all columns in index
```

### 3.3 Partial Indexes

```sql
-- Only index active users (smaller index, faster)
CREATE INDEX idx_active_users ON users(email) 
WHERE status = 'active';

-- Query benefits:
SELECT * FROM users WHERE status = 'active' AND email = 'user@example.com';
-- Uses smaller index, faster lookup
```

### 3.4 Index Maintenance

```sql
-- Analyze index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE 'pg_%';

-- Rebuild fragmented indexes
REINDEX INDEX CONCURRENTLY idx_user_email;

-- Update statistics
ANALYZE users;
```

---

## 4. Advanced Query Patterns

### 4.1 Efficient Pagination

```sql
-- ❌ BAD: O(n log n) - sorts all rows, then skips
SELECT * FROM orders 
ORDER BY created_at DESC 
LIMIT 10 OFFSET 1000;

-- ✅ GOOD: O(k log n) - uses index, only fetches needed rows
SELECT * FROM orders 
WHERE created_at < '2024-01-01'  -- Cursor from previous page
ORDER BY created_at DESC 
LIMIT 10;

-- ✅ BETTER: Keyset pagination
SELECT * FROM orders 
WHERE (created_at, id) < ('2024-01-01', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 10;
```

### 4.2 Efficient Top-N Queries

```sql
-- ❌ BAD: O(n log n) - sorts entire table
SELECT * FROM orders 
ORDER BY total DESC 
LIMIT 10;

-- ✅ GOOD: O(n) - if index exists
CREATE INDEX idx_total_desc ON orders(total DESC);
SELECT * FROM orders 
ORDER BY total DESC 
LIMIT 10;

-- ✅ BEST: Using window functions for per-group top-N
SELECT * FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total DESC) as rn
    FROM orders
) ranked
WHERE rn <= 10;
```

### 4.3 Efficient Duplicate Detection

```sql
-- ❌ BAD: O(n²) - self-join
SELECT DISTINCT a.id, a.email
FROM users a
INNER JOIN users b ON a.email = b.email AND a.id < b.id;

-- ✅ GOOD: O(n log n) - window function
SELECT id, email
FROM (
    SELECT 
        id,
        email,
        ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) as rn
    FROM users
) ranked
WHERE rn = 1;

-- ✅ BEST: O(n) - if unique index exists
CREATE UNIQUE INDEX idx_email_unique ON users(email);
-- Prevents duplicates at insert time
```

---

## 5. Window Functions & Modern SQL

### 5.1 Window Functions Performance

**Basic Window Functions:**

```sql
-- ROW_NUMBER, RANK, DENSE_RANK - O(n log n)
SELECT 
    id,
    name,
    total,
    ROW_NUMBER() OVER (ORDER BY total DESC) as rank,
    RANK() OVER (ORDER BY total DESC) as rank_with_ties,
    DENSE_RANK() OVER (ORDER BY total DESC) as dense_rank
FROM orders;

-- LAG, LEAD - O(n) - single pass
SELECT 
    id,
    created_at,
    total,
    LAG(total) OVER (ORDER BY created_at) as previous_total,
    LEAD(total) OVER (ORDER BY created_at) as next_total
FROM orders;
```

**Partitioned Window Functions:**

```sql
-- Per-user ranking - O(n log n) where n is orders per user
SELECT 
    user_id,
    id,
    total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total DESC) as user_rank
FROM orders;

-- ✅ Optimized with index:
CREATE INDEX idx_user_total ON orders(user_id, total DESC);
```

**Aggregate Window Functions:**

```sql
-- Running totals - O(n) - single pass
SELECT 
    id,
    created_at,
    total,
    SUM(total) OVER (ORDER BY created_at) as running_total,
    AVG(total) OVER (
        PARTITION BY user_id 
        ORDER BY created_at 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg
FROM orders;
```

### 5.2 Modern SQL: FILTER Clause

```sql
-- ✅ Modern: O(n) - single aggregation pass
SELECT 
    user_id,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_count,
    COUNT(*) FILTER (WHERE status = 'pending') as pending_count,
    SUM(total) FILTER (WHERE status = 'completed') as completed_total
FROM orders
GROUP BY user_id;

-- ❌ Old way: O(n) - multiple passes
SELECT 
    user_id,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_count,
    SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END) as completed_total
FROM orders
GROUP BY user_id;
```

### 5.3 Modern SQL: LATERAL Joins

```sql
-- ✅ LATERAL join - O(n*k) where k is subquery result size
SELECT 
    u.id,
    u.name,
    o.id as order_id,
    o.total
FROM users u
CROSS JOIN LATERAL (
    SELECT id, total
    FROM orders
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) o;

-- More efficient than correlated subquery for top-N per group
```

---

## 6. CTEs and Recursive Queries

### 6.1 Common Table Expressions (CTEs)

**Simple CTEs:**

```sql
-- ✅ CTE for readability and potential optimization
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
),
user_orders AS (
    SELECT 
        u.id,
        u.name,
        COUNT(o.id) as order_count
    FROM active_users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.name
)
SELECT * FROM user_orders WHERE order_count > 10;

-- Note: CTEs are materialized in some databases, computed in others
```

**Recursive CTEs:**

```sql
-- ✅ Hierarchical queries - O(n) where n is tree depth
WITH RECURSIVE org_tree AS (
    -- Base case
    SELECT 
        id,
        name,
        parent_id,
        1 as level,
        ARRAY[id] as path
    FROM organizations
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT 
        o.id,
        o.name,
        o.parent_id,
        ot.level + 1,
        ot.path || o.id
    FROM organizations o
    INNER JOIN org_tree ot ON o.parent_id = ot.id
    WHERE NOT o.id = ANY(ot.path)  -- Prevent cycles
)
SELECT * FROM org_tree ORDER BY level, name;
```

**Performance Considerations:**

```sql
-- ❌ BAD: CTE computed multiple times
WITH expensive_cte AS (
    SELECT * FROM large_table WHERE complex_condition()
)
SELECT * FROM expensive_cte WHERE condition1
UNION ALL
SELECT * FROM expensive_cte WHERE condition2;

-- ✅ GOOD: Materialize if used multiple times
CREATE TEMPORARY TABLE temp_expensive AS
SELECT * FROM large_table WHERE complex_condition();
SELECT * FROM temp_expensive WHERE condition1
UNION ALL
SELECT * FROM temp_expensive WHERE condition2;
```

---

## 7. Join Optimization

### 7.1 Join Types and Performance

**INNER JOIN:**

```sql
-- ✅ O(n log m) - if index on join key
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- Index needed:
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_status ON users(status);
```

**LEFT JOIN:**

```sql
-- ✅ O(n log m) - preserves left table rows
SELECT u.name, COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- ⚠️ Filter on right table in WHERE vs ON:
-- WHERE filters after join (reduces to INNER JOIN)
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';  -- ❌ Removes users without orders

-- ON filters during join (preserves LEFT JOIN)
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'completed';  -- ✅
```

**CROSS JOIN (Cartesian Product):**

```sql
-- ⚠️ O(n*m) - use with caution
SELECT u.name, p.name
FROM users u
CROSS JOIN products p
WHERE u.region = p.region;  -- Always filter!

-- ✅ Better: Use INNER JOIN with condition
SELECT u.name, p.name
FROM users u
INNER JOIN products p ON u.region = p.region;
```

### 7.2 Join Order Optimization

```sql
-- Query optimizer usually handles this, but you can influence:

-- ✅ Put most selective table first
SELECT *
FROM small_table s           -- 100 rows
INNER JOIN large_table l ON s.id = l.small_id;  -- 1M rows

-- ✅ Filter before joining
SELECT *
FROM (SELECT * FROM users WHERE status = 'active') u
INNER JOIN orders o ON u.id = o.user_id;
```

### 7.3 Hash Joins vs Nested Loops

```sql
-- Database chooses automatically, but you can hint:

-- PostgreSQL: Force hash join for large tables
SET enable_nestloop = off;
SELECT * FROM large_table1 l1
INNER JOIN large_table2 l2 ON l1.id = l2.id;

-- MySQL: Use STRAIGHT_JOIN to control order
SELECT * FROM small_table s
STRAIGHT_JOIN large_table l ON s.id = l.id;
```

---

## 8. Subquery Optimization

### 8.1 Correlated vs Non-Correlated

```sql
-- ❌ BAD: Correlated subquery - O(n*m)
SELECT 
    u.id,
    u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- ✅ GOOD: JOIN with aggregation - O(n)
SELECT 
    u.id,
    u.name,
    COALESCE(o.order_count, 0) as order_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

### 8.2 EXISTS vs IN vs JOIN

```sql
-- EXISTS - O(n) - stops at first match
SELECT u.*
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.user_id = u.id AND o.total > 1000
);

-- IN - O(n log m) - may be optimized to hash join
SELECT u.*
FROM users u
WHERE u.id IN (SELECT user_id FROM orders WHERE total > 1000);

-- JOIN - O(n) - usually most efficient
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 1000;
```

### 8.3 Scalar Subqueries

```sql
-- ❌ BAD: Scalar subquery in SELECT - O(n*m)
SELECT 
    id,
    name,
    (SELECT MAX(total) FROM orders WHERE user_id = u.id) as max_order
FROM users u;

-- ✅ GOOD: Window function or JOIN - O(n log n)
SELECT 
    u.id,
    u.name,
    MAX(o.total) OVER (PARTITION BY o.user_id) as max_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

---

## 9. Aggregation & Grouping

### 9.1 Efficient GROUP BY

```sql
-- ✅ Use covering index for GROUP BY
CREATE INDEX idx_user_status_created ON orders(user_id, status, created_at);

SELECT user_id, status, COUNT(*), SUM(total)
FROM orders
GROUP BY user_id, status;

-- ✅ Filter before grouping
SELECT user_id, COUNT(*)
FROM orders
WHERE created_at > '2024-01-01'
GROUP BY user_id;
```

### 9.2 HAVING vs WHERE

```sql
-- ❌ BAD: Filtering in HAVING - processes all groups
SELECT user_id, COUNT(*) as cnt
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 10;

-- ✅ GOOD: Filter in WHERE when possible
SELECT user_id, COUNT(*) as cnt
FROM orders
WHERE status = 'completed'  -- Filter rows before grouping
GROUP BY user_id
HAVING COUNT(*) > 10;       -- Filter groups after aggregation
```

### 9.3 Advanced Aggregations

```sql
-- ✅ Modern: ARRAY_AGG, JSON_AGG - O(n)
SELECT 
    user_id,
    ARRAY_AGG(DISTINCT status ORDER BY status) as statuses,
    JSON_AGG(
        JSON_BUILD_OBJECT('id', id, 'total', total)
        ORDER BY total DESC
    ) as orders_json
FROM orders
GROUP BY user_id;

-- ✅ Window aggregates for running calculations
SELECT 
    user_id,
    created_at,
    total,
    SUM(total) OVER (PARTITION BY user_id ORDER BY created_at) as running_total,
    AVG(total) OVER (PARTITION BY user_id) as user_avg
FROM orders;
```

---

## 10. Time Complexity Analysis

### 10.1 Common Operations Complexity

| Operation | Best Case | Average Case | Worst Case | Notes |
|-----------|-----------|--------------|------------|-------|
| Index Lookup | O(log n) | O(log n) | O(log n) | B-tree index |
| Hash Lookup | O(1) | O(1) | O(n) | Hash collision |
| Full Table Scan | O(n) | O(n) | O(n) | No index |
| Sort | O(n log n) | O(n log n) | O(n log n) | Merge/Quick sort |
| JOIN (Indexed) | O(n log m) | O(n log m) | O(n*m) | m = right table |
| JOIN (Hash) | O(n+m) | O(n+m) | O(n*m) | Hash table build |
| GROUP BY | O(n) | O(n log n) | O(n log n) | With/without index |
| DISTINCT | O(n) | O(n log n) | O(n log n) | Hash vs sort |

### 10.2 Query Complexity Examples

**Example 1: Simple Lookup**
```sql
-- O(log n) - Index lookup
SELECT * FROM users WHERE id = 123;
-- Index: PRIMARY KEY (id)
```

**Example 2: Range Query**
```sql
-- O(log n + k) - Index range scan, k = result size
SELECT * FROM orders 
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
-- Index: idx_created ON orders(created_at)
```

**Example 3: Join Query**
```sql
-- O(n log m) - n scans, each O(log m) lookup
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
-- Index: idx_orders_user_id ON orders(user_id)
-- Complexity: O(users * log(orders))
```

**Example 4: Aggregation**
```sql
-- O(n log n) - Sort for grouping
SELECT user_id, COUNT(*), SUM(total)
FROM orders
GROUP BY user_id;
-- If index on user_id: O(n) - sequential scan with grouping
```

**Example 5: Window Function**
```sql
-- O(n log n) - Sort for window
SELECT 
    id,
    total,
    ROW_NUMBER() OVER (ORDER BY total DESC) as rank
FROM orders;
-- If index on total DESC: O(n) - index scan
```

### 10.3 Optimizing Query Complexity

```sql
-- ❌ O(n²) - Nested loop join without index
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id;

-- ✅ O(n log m) - Index on join key
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- ✅ O(n+m) - Hash join for large tables
-- Database optimizer chooses automatically
```

---

## 11. Execution Plans & Profiling

### 11.1 Understanding Execution Plans

**PostgreSQL (EXPLAIN ANALYZE):**

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- Output analysis:
-- Seq Scan on users - O(n) - full table scan (BAD)
-- Index Scan using idx_user_status - O(log n) - index scan (GOOD)
-- Hash Join - O(n+m) - hash join (GOOD for large tables)
-- Nested Loop - O(n*m) - nested loop (BAD for large tables)
```

**MySQL (EXPLAIN):**

```sql
EXPLAIN FORMAT=JSON
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- Key metrics:
-- type: ALL (full scan), index (index scan), ref (index lookup)
-- rows: Estimated rows examined
-- Extra: Using index (covering index), Using filesort (needs sort)
```

### 11.2 Query Profiling

**PostgreSQL:**

```sql
-- Enable timing
\timing on

-- Profile query
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)
SELECT * FROM large_table WHERE condition;

-- Check query statistics
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

**MySQL:**

```sql
-- Enable profiling
SET profiling = 1;

-- Run query
SELECT * FROM large_table WHERE condition;

-- Show profile
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- Check slow query log
-- Set in my.cnf:
-- slow_query_log = 1
-- long_query_time = 1
```

### 11.3 Identifying Bottlenecks

```sql
-- Find slow queries
SELECT 
    query,
    calls,
    total_exec_time / calls as avg_time,
    max_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 1000  -- > 1 second
ORDER BY total_exec_time DESC;

-- Find missing indexes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100  -- High cardinality
  AND correlation < 0.1;  -- Low correlation (random order)
```

---

## 12. Database-Specific Optimizations

### 12.1 PostgreSQL Optimizations

**Connection Pooling:**
```sql
-- Use connection pooler (PgBouncer)
-- Reduces connection overhead
```

**Vacuum and Analyze:**
```sql
-- Regular maintenance
VACUUM ANALYZE users;

-- Aggressive vacuum for large tables
VACUUM FULL users;

-- Auto-vacuum configuration
ALTER TABLE users SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);
```

**PostgreSQL-Specific Features:**
```sql
-- Partial indexes
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Expression indexes
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- GIN indexes for arrays/JSONB
CREATE INDEX idx_tags_gin ON products USING GIN(tags);
CREATE INDEX idx_data_jsonb ON products USING GIN(data jsonb_path_ops);

-- BRIN indexes for large sequential data
CREATE INDEX idx_created_brin ON orders USING BRIN(created_at);
```

### 12.2 MySQL Optimizations

**InnoDB Settings:**
```sql
-- Buffer pool size (main memory for data)
SET GLOBAL innodb_buffer_pool_size = 1073741824;  -- 1GB

-- Query cache (MySQL 5.7 and earlier)
SET GLOBAL query_cache_size = 67108864;  -- 64MB

-- Index hints
SELECT * FROM users USE INDEX (idx_email) WHERE email = 'user@example.com';
SELECT * FROM users FORCE INDEX (idx_email) WHERE email = 'user@example.com';
```

**MySQL-Specific Features:**
```sql
-- Covering index (all columns in index)
CREATE INDEX idx_covering ON orders(user_id, status, total, created_at);
-- Query can use index only
SELECT user_id, status, total FROM orders WHERE user_id = 123;

-- Partitioning
CREATE TABLE orders (
    id INT,
    user_id INT,
    created_at DATE,
    total DECIMAL(10,2)
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 12.3 SQL Server Optimizations

```sql
-- Include columns in index
CREATE INDEX idx_user_status 
ON orders(user_id, status) 
INCLUDE (total, created_at);

-- Filtered indexes
CREATE INDEX idx_active_orders 
ON orders(user_id) 
WHERE status = 'active';

-- Query hints
SELECT * FROM users WITH (INDEX(idx_email)) WHERE email = 'user@example.com';
```

---

## 13. JSON & Modern Data Types

### 13.1 JSON Queries

**PostgreSQL JSONB:**

```sql
-- ✅ Indexed JSON queries - O(log n)
CREATE INDEX idx_data_jsonb ON products USING GIN(data jsonb_path_ops);

-- Query JSON
SELECT * FROM products 
WHERE data->>'category' = 'electronics'
  AND (data->'price')::numeric > 100;

-- JSON aggregation
SELECT 
    user_id,
    JSON_AGG(
        JSON_BUILD_OBJECT('id', id, 'total', total)
        ORDER BY total DESC
    ) as orders
FROM orders
GROUP BY user_id;
```

**MySQL JSON:**

```sql
-- ✅ Indexed JSON queries
CREATE INDEX idx_category ON products((CAST(data->'$.category' AS CHAR(255))));

-- Query JSON
SELECT * FROM products 
WHERE JSON_EXTRACT(data, '$.category') = 'electronics'
  AND JSON_EXTRACT(data, '$.price') > 100;

-- JSON functions
SELECT 
    JSON_OBJECT('id', id, 'name', name) as user_json
FROM users;
```

### 13.2 Array Operations

**PostgreSQL Arrays:**

```sql
-- ✅ GIN index for array searches
CREATE INDEX idx_tags_gin ON products USING GIN(tags);

-- Array queries
SELECT * FROM products WHERE 'electronics' = ANY(tags);
SELECT * FROM products WHERE tags @> ARRAY['electronics', 'sale'];

-- Array aggregation
SELECT 
    user_id,
    ARRAY_AGG(DISTINCT status ORDER BY status) as statuses
FROM orders
GROUP BY user_id;
```

### 13.3 Full-Text Search

**PostgreSQL:**

```sql
-- ✅ GIN index for full-text search
CREATE INDEX idx_content_fts ON articles USING GIN(to_tsvector('english', content));

-- Full-text queries
SELECT * FROM articles 
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'database & performance');

-- Ranking
SELECT 
    title,
    ts_rank(to_tsvector('english', content), query) as rank
FROM articles, to_tsquery('english', 'database') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC;
```

**MySQL:**

```sql
-- ✅ Full-text index
CREATE FULLTEXT INDEX idx_content_fts ON articles(content);

-- Full-text queries
SELECT * FROM articles 
WHERE MATCH(content) AGAINST('database performance' IN NATURAL LANGUAGE MODE);

-- Boolean mode
SELECT * FROM articles 
WHERE MATCH(content) AGAINST('+database +performance' IN BOOLEAN MODE);
```

---

## 14. Partitioning & Sharding

### 14.1 Table Partitioning

**Range Partitioning:**

```sql
-- ✅ Partition by date - O(log n) per partition
CREATE TABLE orders (
    id INT,
    user_id INT,
    created_at DATE,
    total DECIMAL(10,2)
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025)
);

-- Query only scans relevant partition
SELECT * FROM orders WHERE created_at = '2024-06-15';
-- Only scans p2024 partition
```

**Hash Partitioning:**

```sql
-- ✅ Distribute load evenly
CREATE TABLE users (
    id INT,
    name VARCHAR(255),
    email VARCHAR(255)
) PARTITION BY HASH(id) PARTITIONS 4;

-- Query automatically routes to correct partition
SELECT * FROM users WHERE id = 123;
```

**List Partitioning:**

```sql
-- ✅ Partition by discrete values
CREATE TABLE orders (
    id INT,
    status VARCHAR(50),
    total DECIMAL(10,2)
) PARTITION BY LIST (status) (
    PARTITION p_pending VALUES IN ('pending'),
    PARTITION p_completed VALUES IN ('completed', 'shipped'),
    PARTITION p_other VALUES IN (DEFAULT)
);
```

### 14.2 Partition Pruning

```sql
-- ✅ Automatic partition pruning
SELECT * FROM orders 
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
-- Only scans 2024 partition

-- ❌ No pruning - scans all partitions
SELECT * FROM orders 
WHERE YEAR(created_at) = 2024;
-- Use direct date comparison instead
```

---

## 15. Best Practices & Anti-Patterns

### 15.1 Best Practices

**1. Always Use Indexes on JOIN Keys**
```sql
-- ✅
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT * FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

**2. Use Parameterized Queries**
```sql
-- ✅ Prevents SQL injection, enables plan caching
PREPARE get_user AS SELECT * FROM users WHERE id = $1;
EXECUTE get_user(123);
```

**3. Limit Result Sets**
```sql
-- ✅ Always use LIMIT for large result sets
SELECT * FROM orders ORDER BY created_at DESC LIMIT 100;
```

**4. Use Appropriate Data Types**
```sql
-- ✅ Use smallest appropriate type
CREATE TABLE users (
    id SMALLINT,           -- Instead of INT if < 32767
    status VARCHAR(20),   -- Instead of TEXT
    created_at TIMESTAMP   -- Instead of VARCHAR
);
```

**5. Normalize Properly**
```sql
-- ✅ Normalize to reduce redundancy
-- But denormalize for read performance when needed
```

### 15.2 Anti-Patterns to Avoid

**1. SELECT * in Production**
```sql
-- ❌ BAD
SELECT * FROM users;

-- ✅ GOOD
SELECT id, name, email FROM users;
```

**2. Functions on Indexed Columns**
```sql
-- ❌ BAD - Can't use index
SELECT * FROM users WHERE UPPER(email) = 'USER@EXAMPLE.COM';

-- ✅ GOOD - Function-based index or normalized column
CREATE INDEX idx_email_upper ON users(UPPER(email));
SELECT * FROM users WHERE UPPER(email) = 'USER@EXAMPLE.COM';
```

**3. N+1 Query Problem**
```sql
-- ❌ BAD - N+1 queries
FOR user IN users:
    orders = SELECT * FROM orders WHERE user_id = user.id

-- ✅ GOOD - Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

**4. Implicit Type Conversions**
```sql
-- ❌ BAD - String comparison instead of date
SELECT * FROM orders WHERE created_at = '2024-01-01';

-- ✅ GOOD - Proper date type
SELECT * FROM orders WHERE created_at = DATE '2024-01-01';
```

**5. Unnecessary DISTINCT**
```sql
-- ❌ BAD - If JOIN already unique
SELECT DISTINCT u.id, u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- ✅ GOOD - Remove DISTINCT if not needed
SELECT u.id, u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### 15.3 Performance Checklist

- [ ] Indexes on all JOIN keys
- [ ] Indexes on WHERE clause columns
- [ ] Indexes on ORDER BY columns
- [ ] Covering indexes for frequent queries
- [ ] Statistics updated (ANALYZE)
- [ ] Query execution plans reviewed
- [ ] Slow queries identified and optimized
- [ ] Appropriate data types used
- [ ] LIMIT used for large result sets
- [ ] Unnecessary DISTINCT removed
- [ ] Functions on indexed columns avoided
- [ ] Subqueries optimized to JOINs when possible
- [ ] Partitioning considered for large tables
- [ ] Connection pooling configured
- [ ] Regular maintenance (VACUUM, OPTIMIZE)

---

## Advanced Optimization Examples

### Example 1: E-commerce Query Optimization

**Initial Query (Slow):**
```sql
-- ❌ O(n²) - Multiple full scans
SELECT 
    u.id,
    u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
    (SELECT SUM(total) FROM orders o WHERE o.user_id = u.id) as total_spent,
    (SELECT MAX(created_at) FROM orders o WHERE o.user_id = u.id) as last_order
FROM users u
WHERE u.status = 'active';
```

**Optimized Query:**
```sql
-- ✅ O(n log m) - Single pass with aggregation
SELECT 
    u.id,
    u.name,
    COALESCE(o.order_count, 0) as order_count,
    COALESCE(o.total_spent, 0) as total_spent,
    o.last_order
FROM users u
LEFT JOIN (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(total) as total_spent,
        MAX(created_at) as last_order
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
WHERE u.status = 'active';

-- Indexes needed:
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Example 2: Reporting Query Optimization

**Initial Query:**
```sql
-- ❌ O(n log n) - Multiple sorts
SELECT 
    DATE(created_at) as date,
    status,
    COUNT(*) as count,
    SUM(total) as revenue
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at), status
ORDER BY date DESC, status;
```

**Optimized Query:**
```sql
-- ✅ O(n) - Single pass with covering index
CREATE INDEX idx_orders_covering ON orders(created_at, status, total);

SELECT 
    DATE(created_at) as date,
    status,
    COUNT(*) as count,
    SUM(total) as revenue
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at), status
ORDER BY date DESC, status;
-- Uses covering index, no table access needed
```

### Example 3: Top-N Per Group

**Initial Query:**
```sql
-- ❌ O(n²) - Correlated subquery
SELECT o1.*
FROM orders o1
WHERE (
    SELECT COUNT(*) 
    FROM orders o2 
    WHERE o2.user_id = o1.user_id 
      AND o2.total >= o1.total
) <= 3
ORDER BY o1.user_id, o1.total DESC;
```

**Optimized Query:**
```sql
-- ✅ O(n log n) - Window function
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY total DESC
        ) as rn
    FROM orders
) ranked
WHERE rn <= 3;

-- Index for optimal performance:
CREATE INDEX idx_orders_user_total ON orders(user_id, total DESC);
```

---

## Conclusion

### Key Takeaways:

1. **Indexes are Critical** - Proper indexing can reduce O(n) to O(log n)
2. **Avoid Full Scans** - Always filter with indexed columns
3. **JOINs over Subqueries** - Usually more efficient
4. **Use Modern SQL** - Window functions, CTEs, FILTER clause
5. **Understand Complexity** - Know when queries are O(n²) vs O(n log n)
6. **Profile Queries** - Use EXPLAIN to understand execution
7. **Test with Real Data** - Small datasets hide performance issues

### Performance Hierarchy:

1. **O(1)** - Hash lookup (with hash index)
2. **O(log n)** - Index lookup (B-tree index)
3. **O(n)** - Sequential scan (necessary sometimes)
4. **O(n log n)** - Sort/Group by (acceptable for reasonable n)
5. **O(n²)** - Nested loops (avoid when possible)
6. **O(2ⁿ)** - Exponential (never acceptable)

### Next Steps:

1. Profile your slowest queries
2. Add missing indexes
3. Rewrite inefficient queries
4. Monitor query performance
5. Regular maintenance (ANALYZE, VACUUM)
6. Review execution plans regularly

---

*SQL Performance Mastery - Complete Guide*
*Focus on Time Complexity and Modern SQL Features*
*Last Updated: 2024*

