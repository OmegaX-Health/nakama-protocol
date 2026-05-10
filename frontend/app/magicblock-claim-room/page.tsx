// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Metadata } from "next";

import { MagicBlockClaimRoomWorkbench } from "@/components/magicblock-claim-room-workbench";

export const metadata: Metadata = {
  title: "MagicBlock Receipt Verifier | OmegaX Protocol",
  description:
    "A read-only MagicBlock private-review receipt verifier for public-safe OmegaX Protect claim review metadata.",
};

export default function MagicBlockClaimRoomPage() {
  return <MagicBlockClaimRoomWorkbench />;
}
