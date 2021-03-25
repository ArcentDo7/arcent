# Copyright (C) 2020 Adek Maulana
#
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
import time

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from .exceptions import CancelProcess
from .tools import humanbytes, time_formatter


async def progress(current, total, event, start, prog_type, is_cancelled=False):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 15.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Enviando"
        elif "download" in prog_type.lower():
            status = "Baixando"
        else:
            status = "Status"
        progress_str = "**{}:** `[{}{}]` **{}%**".format(
            status,
            "".join("●" for _ in range(math.floor(percentage / 10))),
            "".join("○" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = (
            f"{progress_str}\n"
            f"{humanbytes(current)} de {humanbytes(total)}"
            f" @ {humanbytes(speed)}\n"
            f"**Tempo Estimado:** {time_formatter(eta)}\n"
            f"**Duração:** {time_formatter(elapsed_time)}"
        )
        try:
            await event.edit(f"**{prog_type}**\n\n{tmp}")
        except MessageNotModifiedError:
            pass
