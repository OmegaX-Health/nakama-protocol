// SPDX-License-Identifier: AGPL-3.0-or-later

//! Shared kernel helper module group.

#[cfg(not(feature = "quasar"))]
mod auth;
#[cfg(not(feature = "quasar"))]
mod bindings;
#[cfg(not(feature = "quasar"))]
mod capital_math;
#[cfg(not(feature = "quasar"))]
mod custody;
#[cfg(feature = "quasar")]
mod custody;
#[cfg(not(feature = "quasar"))]
mod fees;
#[cfg(not(feature = "quasar"))]
mod membership;
#[cfg(not(feature = "quasar"))]
mod reserve_accounting;

#[cfg(not(feature = "quasar"))]
pub(crate) use auth::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use bindings::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use capital_math::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use custody::*;
#[cfg(feature = "quasar")]
pub(crate) use custody::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use fees::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use membership::*;
#[cfg(not(feature = "quasar"))]
pub(crate) use reserve_accounting::*;
