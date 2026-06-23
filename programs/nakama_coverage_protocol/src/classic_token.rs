// SPDX-License-Identifier: AGPL-3.0-or-later

//! Local classic SPL-token account wrappers for Anchor account validation.

use crate::platform::*;
use anchor_lang::solana_program::program_pack::Pack;
use std::ops::Deref;

pub type TokenInterface = anchor_spl::token::Token;

#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct TokenAccount(anchor_spl::token::spl_token::state::Account);

impl TokenAccount {
    pub const LEN: usize = anchor_spl::token::spl_token::state::Account::LEN;
}

impl AccountDeserialize for TokenAccount {
    fn try_deserialize_unchecked(buf: &mut &[u8]) -> Result<Self> {
        anchor_spl::token::spl_token::state::Account::unpack(buf)
            .map(TokenAccount)
            .map_err(Into::into)
    }
}

impl AccountSerialize for TokenAccount {}

impl Owner for TokenAccount {
    fn owner() -> Pubkey {
        anchor_spl::token::ID
    }
}

impl Discriminator for TokenAccount {
    const DISCRIMINATOR: &'static [u8] = &[];
}

#[cfg(feature = "idl-build")]
impl IdlBuild for TokenAccount {}

impl Deref for TokenAccount {
    type Target = anchor_spl::token::spl_token::state::Account;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Mint(anchor_spl::token::spl_token::state::Mint);

impl Mint {
    pub const LEN: usize = anchor_spl::token::spl_token::state::Mint::LEN;
}

impl AccountDeserialize for Mint {
    fn try_deserialize_unchecked(buf: &mut &[u8]) -> Result<Self> {
        anchor_spl::token::spl_token::state::Mint::unpack(buf)
            .map(Mint)
            .map_err(Into::into)
    }
}

impl AccountSerialize for Mint {}

impl Owner for Mint {
    fn owner() -> Pubkey {
        anchor_spl::token::ID
    }
}

impl Discriminator for Mint {
    const DISCRIMINATOR: &'static [u8] = &[];
}

#[cfg(feature = "idl-build")]
impl IdlBuild for Mint {}

impl Deref for Mint {
    type Target = anchor_spl::token::spl_token::state::Mint;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
