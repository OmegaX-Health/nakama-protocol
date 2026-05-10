# Founder Reservation Runbook

Founder reservations are public launch holds collected through the OmegaX
website and the OmegaX Health protocol-oracle service. They are paid into one
configured Squads vault with a unique Solana Pay reference per buyer. No custom
waitlist program is deployed for this flow.

## Products

| Campaign id | Public lane | Price | Reservation window |
|-------------|-------------|-------|--------------------|
| `founder-event7` | Event cover | `$39` | 7 days |
| `founder-travel30` | Travel cover | `$99` | 30 days |

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
- Reserve only changes after a later activation/posting flow books funds through
  the normal reserve and premium controls.
- Refunds are manual in v0 and recorded by the operator with a Squads refund
  transaction signature.

## Operator Checklist

1. Configure `PROTECT_RESERVATION_SQUADS_VAULT` in the protocol-oracle service.
2. Pre-create Squads vault token accounts for every enabled SPL mint.
3. Configure mint/decimals and price sources for volatile or project assets.
4. Confirm `/v1/public/reservations/campaigns` returns both campaigns and the
   intended enabled rails.
5. Run a prepare-submit-confirm rehearsal for SOL and one SPL rail on the target
   cluster.
6. Reconcile reservations by unique reference, not by payer memo.

## Fail-Closed Rules

The service must not produce a payable quote when the campaign is paused, token
rail is disabled, the Squads vault is missing, the SPL vault token account is
missing, the quote is stale, or the selected asset has no fresh price. Confirm
must reject underpayment, wrong recipient, wrong token, expired quote, duplicate
signature, and transactions that do not include the reservation reference.
