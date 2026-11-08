#!/usr/bin/env python3
"""SaaS Invoice & Billing PDF Generation Cost Calculator."""
import argparse
import sys

def calculate_invoice_cost(monthly_invoices, peak_ratio=0.7):
    # In SaaS billing, 70% of invoices are generated on the 1st of the month
    peak_invoices = monthly_invoices * peak_ratio
    
    # Self-hosted: Needs auto-scaling instances to prevent timeouts during billing spikes
    if monthly_invoices <= 2000:
        base_cloud = 35.0
    elif monthly_invoices <= 10000:
        base_cloud = 85.0
    elif monthly_invoices <= 30000:
        base_cloud = 180.0
    else:
        base_cloud = 320.0

    # Engineer monitoring billing runs: 2.5 hrs/mo
    billing_ops = 2.5 * 65.0
    self_hosted_total = base_cloud + billing_ops

    # Managed PDF API
    if monthly_invoices <= 1200:
        api_tier = "Lite ($29/mo)"
        api_cost = 29.0
    elif monthly_invoices <= 3000:
        api_tier = "Plus ($49/mo)"
        api_cost = 49.0
    elif monthly_invoices <= 12000:
        api_tier = "Professional ($99/mo)"
        api_cost = 99.0
    else:
        api_tier = "Scale ($199/mo)"
        api_cost = 199.0

    cost_per_doc_self = self_hosted_total / monthly_invoices
    cost_per_doc_api = api_cost / monthly_invoices
    savings = self_hosted_total - api_cost

    return {
        "monthly_invoices": monthly_invoices,
        "peak_invoices": int(peak_invoices),
        "self_hosted_total": self_hosted_total,
        "cost_per_doc_self": cost_per_doc_self,
        "api_tier": api_tier,
        "api_cost": api_cost,
        "cost_per_doc_api": cost_per_doc_api,
        "savings": savings
    }

def main():
    parser = argparse.ArgumentParser(description="SaaS Invoice PDF API Cost Calculator")
    parser.add_argument("--invoices", type=int, default=5000, help="Monthly billing invoices generated (default: 5,000)")
    args = parser.parse_args()

    r = calculate_invoice_cost(args.invoices)
    print("=" * 68)
    print(" SaaS Transactional Invoice PDF Generation Cost Model")
    print("=" * 68)
    print(f" Monthly Invoices             : {r['monthly_invoices']:,} PDFs")
    print(f" Peak Billing Spike (Day 1)   : ~{r['peak_invoices']:,} PDFs generated in burst")
    print(f" Self-Hosted Infrastructure   : ${r['self_hosted_total']:.2f}/mo (${r['cost_per_doc_self']:.4f}/doc)")
    print(f" Managed PDF Generation Plan  : {r['api_tier']} (${r['cost_per_doc_api']:.4f}/doc)")
    print("-" * 68)
    print(f" Net Monthly Savings          : ${r['savings']:.2f}/mo ({(r['savings']/r['self_hosted_total'])*100:.1f}%)")
    print("=" * 68)
    return 0

if __name__ == "__main__":
    sys.exit(main())
