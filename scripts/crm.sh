#!/bin/bash
# AvestAI CRM - Quick query tool
# Usage: ./crm.sh [command]
# Commands: pipeline, leads, customers, revenue, add-contact, sql

DB="$HOME/.openclaw/workspace/data/avestai.db"

case "${1:-pipeline}" in
  pipeline)
    echo "── AvestAI Sales Pipeline ───────────────────────────────"
    sqlite3 -column -header "$DB" "SELECT id, name, COALESCE(company,'—'), status, tier_interest FROM pipeline;"
    ;;
  leads)
    echo "── All Leads ────────────────────────────────────────────"
    sqlite3 -column -header "$DB" "SELECT id, name, email, phone, status, tier_interest FROM leads;"
    ;;
  customers)
    echo "── Active Customers ─────────────────────────────────────"
    sqlite3 -column -header "$DB" "SELECT id, name, tier, price_paid, install_version, next_renewal FROM customers;"
    ;;
  revenue)
    echo "── Revenue Summary ──────────────────────────────────────"
    sqlite3 -column -header "$DB" "SELECT month, type, total, transactions FROM revenue_summary;"
    echo ""
    sqlite3 -column -header "$DB" "SELECT 'Total: $' || COALESCE(SUM(amount),0) as all_time_revenue FROM revenue;"
    ;;
  contacts)
    echo "── Contact Log ──────────────────────────────────────────"
    sqlite3 -column -header "$DB" "
      SELECT l.name, c.contact_date, c.method, c.direction, substr(c.summary,1,50) as summary
      FROM contacts c JOIN leads l ON c.lead_id = l.id
      ORDER BY c.contact_date DESC LIMIT 20;"
    ;;
  history)
    # history <lead name or id>
    shift
    sqlite3 -column -header "$DB" "
      SELECT c.contact_date, c.method, c.direction, c.summary, c.next_action
      FROM contacts c JOIN leads l ON c.lead_id = l.id
      WHERE lower(l.name) LIKE lower('%$1%') OR l.id = '$1'
      ORDER BY c.contact_date;"
    ;;
  sql)
    shift
    sqlite3 -column -header "$DB" "$@"
    ;;
  *)
    echo "Usage: crm.sh [pipeline|leads|customers|contacts|history <name>|revenue|sql 'QUERY']"
    ;;
esac
