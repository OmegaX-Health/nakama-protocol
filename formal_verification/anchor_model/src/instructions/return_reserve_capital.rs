// User-owned. Regenerating the spec does NOT overwrite this file.
// Guard checks live in the sibling `crate::guards` module and ARE
// regenerated on every `qedgen codegen`. Drift between the spec
// handler block and the `spec_hash` below fires a compile_error!
// via the `#[qed(verified, ...)]` macro.

use anchor_lang::prelude::*;
use crate::guards;
use qedgen_macros::qed;
use crate::{ReturnReserveCapital, ReturnReserveCapitalArgs};

impl<'info> ReturnReserveCapital<'info> {
    #[qed(verified, spec = "../../omegax_protocol.qedspec", handler = "return_reserve_capital", hash = "ffd8ac7b5096437d", spec_hash = "3e36c39cf4e233a0")]
    #[inline(always)]
    pub fn handler(&mut self, args: ReturnReserveCapitalArgs) -> Result<()> {
        guards::return_reserve_capital(self, args)?;
        // Spec effect (needs fill): funded_amount add_sat 1
        // Spec effect (needs fill): audit_nonce add_sat 1
        // Spec transfer: vault_token_account -> recipient_token_account amount=args.amount
        todo!("fill non-mechanical effects, events, transfers, calls")
    }
}
