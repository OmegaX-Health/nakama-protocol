# Founder Reservation Runbook

Founder reservations are public launch holds collected through the Nakama
website and the Nakama Health protocol-oracle service. They are paid into one
configured Squads vault with a unique Solana Pay reference per buyer. No custom
waitlist program is deployed for this flow.

## Products

| Campaign id | Public lane | Price | Reservation window | Cap mode | Target seats |
|-------------|-------------|-------|--------------------|----------|--------------|
| `founder-event7` | Event cover | `$39` | 7 days | Fixed 3,000 USD cap once active terms are available | 100 |
| `founder-travel30` | Travel cover Founder access | `$99` | 30 days | Reserve-indexed target up to 250,000 USD at activation | 100 |

The Travel cover target is conditional. It is not active cover when the buyer
reserves, and the target max benefit is not available until the posted
claims-paying reserve/backstop reaches the required threshold and binding terms
are published for activation.

Accepted rails are USDC, PUSD, USDT, SOL, WBTC, WETH, and OMEGAX when the
oracle service has a configured/fresh quote and the Squads vault recipient or
token account is available.

## Custody And Reserve Treatment

- Payments go to `PROTECT_RESERVATION_SQUADS_VAULT`.
- Each reservation gets a unique Solana Pay `reference`.
- Invite codes are stored off-chain only and are never included in an on-chain
  memo or payment message.
- Pending reservations are not active cover, not LP deposits, and not
  claims-paying reserve.
- Prediction-market volume, waitlist deposits, and pending reservations never
  count as claims-paying reserve.
- Reserve only changes after a later activation/posting flow books funds through
  the normal reserve and premium controls.
- Refunds are manual in v0 and recorded by the operator with a Squads refund
  transaction signature.

## Operator Checklist

1. Configure `PROTECT_RESERVATION_SQUADS_VAULT` in the protocol-oracle service.
2. Pre-create Squads vault token accounts for every enabled SPL mint.
3. Configure mint/decimals and price sources for volatile or project assets.
4. Confirm `/v1/public/reservations/campaigns` returns both campaigns, the
   intended enabled rails, and the Travel cover fields
   `targetSeatCount=100`, `targetMaxBenefitUsd=250000`,
   `capMode=reserve_indexed`, `capLadder`, and `activationTermsLabel`. The
   current ladder includes the 2,000,000 USD reserve/backstop row that can lock
   a 200,000 USD activation cap before the final 250,000 USD target row.
5. Run a prepare-submit-confirm rehearsal for SOL and one SPL rail on the target
   cluster.
6. Reconcile reservations by unique reference, not by payer memo.

## Fail-Closed Rules

The service must not produce a payable quote when the campaign is paused, token
rail is disabled, the Squads vault is missing, the SPL vault token account is
missing, the quote is stale, or the selected asset has no fresh price. Confirm
must reject underpayment, wrong recipient, wrong token, expired quote, duplicate
signature, and transactions that do not include the reservation reference.

If the Travel cover campaign cannot expose current reserve-indexed cap metadata
or reserve/backstop status, public copy must fail closed: show reservation access
only, never "live 250,000 USD coverage" or active claims-paying reserve.
