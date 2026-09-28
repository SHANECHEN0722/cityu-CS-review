#!/usr/bin/env python3
"""CS6480 Chapter 3: a finite-bid GSP verifier, Python 3.8+, standard library only.
Copyright © 2026 Xiaotie Deng. City University of Hong Kong.
Synthetic course model. This checker is deterministic and is not an AI service.
"""
import argparse
import csv
import io
import json
import sys
import unittest
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

IDS = 'ABCD'
VALUES = (10, 8, 6, 4)
GRID = tuple(range(13))
ALPHA = (F(10,100), F(6,100), F(3,100))
PREDICTED = (F(10,100), F(4,100), F(3,100))
BASELINE = (10, 8, 6, 4)
P = (7, 8, 6, 4)
Q = (10, 6, 4, 2)
HERE = Path(__file__).resolve().parent

def validate(bids):
    if len(bids) != 4 or any(type(b) is not int or b not in GRID for b in bids):
        raise ValueError('Enter four integer bids, each from 0 to 12, in A B C D order.')
    return tuple(bids)

def outcome(bids, ctrs=ALPHA):
    bids = validate(bids)
    if len(ctrs) != 3 or any(c < 0 or c > 1 for c in ctrs):
        raise ValueError('Three CTRs in [0,1] are required.')
    ranked = sorted(range(4), key=lambda i: (-bids[i], i))
    rows = [None]*4
    for rank, i in enumerate(ranked):
        slot = rank+1 if rank<3 else None
        cpc = bids[ranked[rank+1]] if slot else 0
        ctr = ctrs[rank] if slot else F(0)
        rows[i] = dict(agent=IDS[i], value=VALUES[i], bid=bids[i], slot=slot,
                       cpc=cpc, ctr=ctr, utility=ctr*(VALUES[i]-cpc),
                       payment=ctr*cpc)
    return rows

def scan(bids, agent, ctrs=ALPHA):
    bids = validate(bids)
    if agent not in IDS or len(agent) != 1:
        raise ValueError('Agent must be A, B, C or D.')
    i = IDS.index(agent)
    results=[]
    for bid in GRID:
        proposal=list(bids); proposal[i]=bid
        results.append(outcome(proposal,ctrs)[i])
    return results

def audit(bids, ctrs=ALPHA):
    current=outcome(bids,ctrs)
    report=[]
    for i, agent in enumerate(IDS):
        alternatives=scan(bids,agent,ctrs)
        best=max(r['utility'] for r in alternatives)
        report.append(dict(agent=agent, current_utility=current[i]['utility'],
                           best_utility=best, gain=best-current[i]['utility'],
                           best_bids=[r['bid'] for r in alternatives if r['utility']==best]))
    return report

def json_value(x):
    return float(x) if isinstance(x,F) else x

def save_result(case, bids, rows, extra=None):
    dest=HERE/'outputs'; dest.mkdir(exist_ok=True)
    stem=datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'_'+case
    payload=dict(case=case,bids=bids,values=VALUES,permitted_bids=GRID,
                 tie_order=list(IDS),environment_ctrs=ALPHA,
                 units='utility and payment: currency per impression; bid and CPC: currency per click',
                 scope='One-shot pure-strategy GSP, integer bid grid 0..12, fixed rivals in each scan.',
                 results=rows,extra=extra)
    (dest/(stem+'.json')).write_text(json.dumps(payload,default=json_value,indent=2),encoding='utf-8')
    with (dest/(stem+'.csv')).open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({k:json_value(v) for k,v in r.items()} for r in rows)
    print('\nSaved JSON and CSV in:',dest)

def show_outcome(bids):
    rows=outcome(bids)
    print('\nAgent  Value  Bid  Slot  CPC  Expected utility')
    for r in rows:
        print(f"{r['agent']:>3} {r['value']:>7} {r['bid']:>4} {str(r['slot'] or '-'):>5} {r['cpc']:>4} {float(r['utility']):>12.4f}")
    revenue=sum(r['payment'] for r in rows)
    utility=sum(r['utility'] for r in rows)
    print(f'Revenue={float(revenue):.4f}  Total utility={float(utility):.4f}  Advertiser click value={float(revenue+utility):.4f}')
    return rows

def show_audit(bids, label):
    show_outcome(bids)
    rows=audit(bids)
    print('\nAgent  Current utility  Best utility  Gain     Best permitted bids')
    for r in rows:
        print(f"{r['agent']:>3} {float(r['current_utility']):>14.4f} {float(r['best_utility']):>13.4f} {float(r['gain']):>8.4f}  {r['best_bids']}")
    gap=max(r['gain'] for r in rows)
    print(f'\nMaximum gain = {float(gap):.4f}')
    print('VERDICT:', 'PASS: pure Nash equilibrium on the stated bid grid.' if gap==0 else 'FAIL: a profitable permitted unilateral deviation exists.')
    print('The checker holds rival bids fixed separately for each advertiser.')
    save_result(label,bids,rows,dict(maximum_gain=gap,grid_equilibrium=(gap==0)))

def candidate_a(bid):
    validate((bid,8,6,4))
    rows=scan(BASELINE,'A')
    best=max(r['utility'] for r in rows)
    result=rows[bid]
    print('\nA bid  Slot  CPC  Utility')
    for r in rows:
        print(f"{r['bid']:>5} {str(r['slot'] or '-'):>5} {r['cpc']:>4} {float(r['utility']):>8.4f}")
    print(f"\nRecommendation {bid}: utility={float(result['utility']):.4f}; improvement over bid 10={float(result['utility']-F(1,5)):.4f}")
    print(f"Best utility={float(best):.4f}; shortfall={float(best-result['utility']):.4f}")
    print('Best permitted bids:',[r['bid'] for r in rows if r['utility']==best])
    print('This checks A only, not an equilibrium of all four advertisers.')
    save_result('task_A',BASELINE,rows,dict(recommended_bid=bid,shortfall=best-result['utility']))

def prediction_case():
    pred=scan(BASELINE,'A',PREDICTED); true=scan(BASELINE,'A',ALPHA)
    maximum=max(r['utility'] for r in pred)
    chosen=min(r['bid'] for r in pred if r['utility']==maximum)
    actual_max=max(r['utility'] for r in true)
    rows=[dict(bid=b,slot=pred[b]['slot'],cpc=pred[b]['cpc'],predicted_utility=pred[b]['utility'],environment_utility=true[b]['utility']) for b in GRID]
    print('\nPredicted CTRs: 0.10, 0.04, 0.03; environment: 0.10, 0.06, 0.03')
    print('The provided deterministic policy chooses the smallest bid among predicted best bids.')
    print(f'Chosen bid={chosen}; predicted utility={float(maximum):.4f}; environment utility={float(true[chosen]["utility"]):.4f}')
    print(f'Best environment utility={float(actual_max):.4f}; decision shortfall={float(actual_max-true[chosen]["utility"]):.4f}')
    save_result('task_C',BASELINE,rows,dict(predicted_ctrs=PREDICTED,chosen_bid=chosen,decision_shortfall=actual_max-true[chosen]['utility']))

class ModelTests(unittest.TestCase):
    def test_baseline_utilities(self): self.assertEqual([r['utility'] for r in outcome(BASELINE)],[F(1,5),F(3,25),F(3,50),0])
    def test_baseline_prices(self): self.assertEqual([r['cpc'] for r in outcome(BASELINE)],[8,6,4,0])
    def test_baseline_revenue(self): self.assertEqual(sum(r['payment'] for r in outcome(BASELINE)),F(32,25))
    def test_welfare_accounting(self): self.assertEqual(sum(r['payment']+r['utility'] for r in outcome(BASELINE)),F(83,50))
    def test_improving_bid(self): self.assertEqual(outcome(P)[0]['utility'],F(6,25))
    def test_best_bids_a(self): self.assertEqual(audit(BASELINE)[0]['best_bids'],[6,7])
    def test_baseline_gap(self): self.assertEqual(max(r['gain'] for r in audit(BASELINE)),F(1,25))
    def test_p_gap(self): self.assertEqual(max(r['gain'] for r in audit(P)),F(1,50))
    def test_q_gap(self): self.assertEqual(max(r['gain'] for r in audit(Q)),0)
    def test_q_utilities(self): self.assertEqual([r['utility'] for r in outcome(Q)],[F(2,5),F(6,25),F(3,25),0])
    def test_tie_order(self): self.assertEqual([r['slot'] for r in outcome((6,6,6,6))],[1,2,3,None])
    def test_zero_bids(self): self.assertEqual([r['cpc'] for r in outcome((0,0,0,0))],[0,0,0,0])
    def test_negative_utility_allowed(self): self.assertLess(outcome((10,8,6,12))[3]['utility'],0)
    def test_prediction_choice(self):
        rows=scan(BASELINE,'A',PREDICTED); best=max(r['utility'] for r in rows)
        self.assertEqual(min(r['bid'] for r in rows if r['utility']==best),8)
    def test_grid_rejection(self):
        for b in [(-1,8,6,4),(13,8,6,4),(7.5,8,6,4),(True,8,6,4),(1,2,3)]:
            with self.assertRaises(ValueError): validate(b)
    def test_scan_holds_rivals_fixed(self):
        for agent in IDS:
            for r in scan(BASELINE,agent):
                b=list(BASELINE); b[IDS.index(agent)]=r['bid']
                self.assertEqual(r,outcome(b)[IDS.index(agent)])
    def test_independent_payoff_calculation(self):
        # Recompute each player's rank and next bidder without the outcome routine.
        for bids in (BASELINE,P,Q,(0,0,0,0),(12,12,12,12),(4,7,2,8)):
            actual=outcome(bids)
            for i in range(4):
                above=[j for j in range(4) if j!=i and (bids[j]>bids[i] or (bids[j]==bids[i] and j<i))]
                if len(above)>=3: expected=F(0)
                else:
                    below=[j for j in range(4) if j!=i and j not in above]
                    next_bid=max((bids[j] for j in below),default=0)
                    expected=ALPHA[len(above)]*(VALUES[i]-next_bid)
                self.assertEqual(actual[i]['utility'],expected)
    def test_all_gains_nonnegative(self):
        for bids in (BASELINE,P,Q,(0,0,0,0),(12,12,12,12)):
            self.assertTrue(all(r['gain']>=0 for r in audit(bids)))

def self_test():
    buffer=io.StringIO()
    result=unittest.TextTestRunner(stream=buffer,verbosity=0).run(unittest.defaultTestLoader.loadTestsFromTestCase(ModelTests))
    if not result.wasSuccessful():
        print(buffer.getvalue()); raise RuntimeError('Model tests failed. Stop and contact the instructor.')
    print(f'READY: {result.testsRun} Chapter 3 tests passed.')

MENU='''
1 Baseline outcome
2 Task A: check an AI-recommended bid for A
3 Task B: audit candidate P = (7, 8, 6, 4)
4 Task B: audit candidate Q = (10, 6, 4, 2)
5 Task C: predicted CTRs versus environment CTRs
6 Audit your own four-bid profile
7 Run the 18 tests again
0 Exit
'''

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--test',action='store_true')
    parser.add_argument('--case',choices=['baseline','a','p','q','prediction'])
    parser.add_argument('--bid',type=int,default=7)
    args=parser.parse_args()
    self_test()
    if args.test: return
    print('CS6480 Chapter 3. All bids are integers 0..12. Ties: A, B, C, D.')
    print('Select: is waiting for your choice. Type a menu number and press Return.')
    if args.case:
        if args.case=='baseline': save_result('baseline',BASELINE,show_outcome(BASELINE))
        elif args.case=='a': candidate_a(args.bid)
        elif args.case=='p': show_audit(P,'candidate_P')
        elif args.case=='q': show_audit(Q,'candidate_Q')
        else: prediction_case()
        return
    while True:
        print(MENU)
        try:
            choice=input('Select: ').strip()
            if choice=='0': print('Session ended. Your results remain in Lab/outputs.'); return
            if choice=='1': save_result('baseline',BASELINE,show_outcome(BASELINE))
            elif choice=='2': candidate_a(int(input('AI-recommended bid for A (integer 0..12): ').strip()))
            elif choice=='3': show_audit(P,'candidate_P')
            elif choice=='4': show_audit(Q,'candidate_Q')
            elif choice=='5': prediction_case()
            elif choice=='6': show_audit(tuple(map(int,input('Bids for A B C D, separated by spaces: ').split())),'custom')
            elif choice=='7': self_test()
            else: print('Please choose a menu number from 0 to 7.')
        except (ValueError,TypeError) as err: print('Input problem:',err)
        except EOFError: print('\nInput closed. Restart the launcher to continue.'); return

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt: print('\nSession ended. No input files were changed.'); sys.exit(0)
