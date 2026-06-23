// User-owned. Regenerating the spec does NOT overwrite this file.
// Guard checks live in the sibling `crate::guards` module and ARE
// regenerated on every `qedgen codegen`. Drift between the spec
// handler block and the `spec_hash` below fires a compile_error!
// via the `#[qed(verified, ...)]` macro.

use anchor_lang::prelude::*;
use crate::guards;
use qedgen_macros::qed;
use crate::{RecordReserveEarnings, RecordReserveEarningsArgs};

impl<'info> RecordReserveEarnings<'info> {
    #[qed(verified, spec = "../../nakama_coverage_protocol.qedspec", handler = "record_reserve_earnings", hash = "c3dd874b90d109f0", spec_hash = "264ef3256e76dde0")]
    #[inline(always)]
    pub fn handler(&mut self, args: RecordReserveEarningsArgs) -> Result<()> {
        guards::record_reserve_earnings(self, args)?;
        // Spec effect (needs fill): funded_amount add_sat 1
        // Spec effect (needs fill): audit_nonce add_sat 1
        // Spec transfer: source_token_account -> vault_token_account amount=args.amount
        todo!("fill non-mechanical effects, events, transfers, calls")
    }
}
