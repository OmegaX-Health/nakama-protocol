import Lake
open Lake DSL

package omegaxProtocolProofs

require qedgenSupport from
  "./lean_solana"

require qedgenSupportMathlib from
  "./lean_solana_mathlib"

@[default_target]
lean_lib OmegaxProtocolSpec where
  roots := #[`Spec, `Proofs]
