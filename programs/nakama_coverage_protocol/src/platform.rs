// SPDX-License-Identifier: AGPL-3.0-or-later

//! Framework-facing protocol imports.
//!
//! The protocol is being migrated from Anchor to Quasar. Keep implementation
//! modules importing this local seam so the framework swap happens here instead
//! of through scattered direct prelude imports.

#[cfg(not(feature = "quasar"))]
pub use anchor_lang::{
    account, error_code, event, prelude::*, require, require_eq, require_keys_eq, Accounts,
    AnchorDeserialize, AnchorSerialize, InitSpace,
};

#[cfg(feature = "quasar")]
pub use quasar_lang::prelude::*;

#[cfg(feature = "quasar")]
pub type Result<T = (), E = ProgramError> = core::result::Result<T, E>;

#[cfg(feature = "quasar")]
pub type Pubkey = Address;

#[cfg(feature = "quasar")]
macro_rules! error {
    ($error:expr $(,)?) => {
        ProgramError::from($error)
    };
}

#[cfg(feature = "quasar")]
pub(crate) use error;

#[cfg(feature = "quasar")]
macro_rules! err {
    ($error:expr $(,)?) => {
        Err(ProgramError::from($error))
    };
}

#[cfg(feature = "quasar")]
pub(crate) use err;

#[cfg(feature = "quasar")]
macro_rules! require_keys_neq {
    ($left:expr, $right:expr, $error:expr $(,)?) => {
        if quasar_lang::keys_eq(&$left, &$right) {
            return Err($error.into());
        }
    };
}

#[cfg(feature = "quasar")]
pub(crate) use require_keys_neq;

#[cfg(feature = "quasar")]
pub use quasar_spl::{InterfaceAccount, Mint, Token as TokenAccount, TokenInterface};

#[cfg(feature = "quasar")]
#[inline(always)]
pub fn quasar_pda_matches(
    expected: &Address,
    program_id: &Address,
    seeds: &[&[u8]],
    bump: u8,
) -> bool {
    if seeds.len() >= 17 || seeds.iter().any(|seed| seed.len() > 32) {
        return false;
    }

    let bump_seed = [bump];
    let mut full_seeds: [&[u8]; 17] = [&[]; 17];
    let mut index = 0;
    while index < seeds.len() {
        full_seeds[index] = seeds[index];
        index += 1;
    }
    full_seeds[index] = &bump_seed;

    quasar_lang::pda::verify_program_address(&full_seeds[..=index], program_id, expected).is_ok()
}

#[cfg(feature = "quasar")]
#[inline(always)]
pub fn quasar_pda_matches_canonical(
    expected: &Address,
    program_id: &Address,
    seeds: &[&[u8]],
) -> bool {
    if seeds.len() > 16 || seeds.iter().any(|seed| seed.len() > 32) {
        return false;
    }

    match quasar_lang::pda::based_try_find_program_address(seeds, program_id) {
        Ok((address, _bump)) => quasar_lang::keys_eq(&address, expected),
        Err(_) => false,
    }
}
