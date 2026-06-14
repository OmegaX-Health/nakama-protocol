// User-owned. Regenerating the spec does NOT overwrite this file.
// Guard checks live in the sibling `crate::guards` module and ARE
// regenerated on every `qedgen codegen`. Drift between the spec
// handler block and the `spec_hash` below fires a compile_error!
// via the `#[qed(verified, ...)]` macro.

use anchor_lang::prelude::*;
use crate::guards;
use qedgen_macros::qed;
use crate::{DepositReserveCapital, DepositReserveCapitalArgs};

impl<'info> DepositReserveCapital<'info> {
    #[qed(verified, spec = "../../omegax_protocol.qedspec", handler = "deposit_reserve_capital", hash = "2e59555e1859b51c", spec_hash = "4ca58a8df152497e")]
    #[inline(always)]
    pub fn handler(&mut self, args: DepositReserveCapitalArgs) -> Result<()> {
        guards::deposit_reserve_capital(self, args)?;
        // Spec effect (needs fill): funded_amount add_sat 1
        // Spec effect (needs fill): audit_nonce add_sat 1
        // Spec transfer: source_token_account -> vault_token_account amount=args.amount
        todo!("fill non-mechanical effects, events, transfers, calls")
    }
}
