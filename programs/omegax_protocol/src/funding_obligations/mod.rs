// SPDX-License-Identifier: AGPL-3.0-or-later

//! Funding-line and obligation instruction module group.

#[cfg(not(feature = "quasar"))]
use crate::classic_token::{Mint, TokenAccount, TokenInterface};
use crate::platform::*;

use crate::args::*;
use crate::constants::*;
use crate::errors::*;
use crate::events::*;
use crate::kernel::*;
use crate::state::*;
use crate::types::*;

mod funding_lines;
mod inflows;
mod obligations;
mod reserves;
mod settlement;

#[cfg(not(feature = "quasar"))]
pub(crate) use funding_lines::open_funding_line;
#[cfg(feature = "quasar")]
pub(crate) use funding_lines::open_funding_line;
#[cfg(not(feature = "quasar"))]
pub(crate) use inflows::{
    deposit_reserve_capital, fund_sponsor_budget, record_premium_payment, record_reserve_earnings,
    return_reserve_capital,
};
#[cfg(feature = "quasar")]
pub(crate) use inflows::{
    deposit_reserve_capital, fund_sponsor_budget, record_premium_payment, record_reserve_earnings,
    return_reserve_capital,
};
#[cfg(not(feature = "quasar"))]
pub(crate) use obligations::create_obligation;
#[cfg(feature = "quasar")]
pub(crate) use obligations::create_obligation;
#[cfg(feature = "quasar")]
pub(crate) use reserves::{release_reserve, reserve_obligation};
#[cfg(not(feature = "quasar"))]
pub(crate) use reserves::{release_reserve, reserve_obligation};
#[cfg(not(feature = "quasar"))]
pub(crate) use settlement::settle_obligation;
#[cfg(feature = "quasar")]
pub(crate) use settlement::settle_obligation;

pub use funding_lines::OpenFundingLine;
pub use inflows::{
    DepositReserveCapital, FundSponsorBudget, RecordPremiumPayment, RecordReserveEarnings,
    ReturnReserveCapital,
};
pub use obligations::CreateObligation;
pub use reserves::{ReleaseReserve, ReserveObligation};
pub use settlement::SettleObligation;

#[cfg(not(feature = "quasar"))]
pub(crate) use funding_lines::__client_accounts_open_funding_line;
#[cfg(not(feature = "quasar"))]
pub(crate) use inflows::{
    __client_accounts_deposit_reserve_capital, __client_accounts_fund_sponsor_budget,
    __client_accounts_record_premium_payment, __client_accounts_record_reserve_earnings,
    __client_accounts_return_reserve_capital,
};
#[cfg(not(feature = "quasar"))]
pub(crate) use obligations::__client_accounts_create_obligation;
#[cfg(not(feature = "quasar"))]
pub(crate) use reserves::{
    __client_accounts_release_reserve, __client_accounts_reserve_obligation,
};
#[cfg(not(feature = "quasar"))]
pub(crate) use settlement::__client_accounts_settle_obligation;
