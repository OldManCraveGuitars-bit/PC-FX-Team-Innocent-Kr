#!/usr/bin/env python3
"""Windows desktop patcher for the Team Innocent KR v0.735 test release."""
from __future__ import annotations

import argparse
import os
import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from apply_patch import BASE, CUE, PatchCancelled, apply_patch, read_patch

BG = "#f5f7fb"
INK = "#172b44"
MUTED = "#52637a"
ACCENT = "#1465b8"
BORDER = "#dce4ee"
WHITE = "#ffffff"


def available_output(parent: Path) -> Path:
    first = parent / "Team Innocent KR v0.735"
    if not first.exists():
        return first
    for number in range(2, 1000):
        candidate = parent / f"Team Innocent KR v0.735 ({number})"
        if not candidate.exists():
            return candidate
    raise RuntimeError("출력 폴더 이름을 정할 수 없습니다. 다른 위치를 선택해 주세요.")


def friendly_error(error: Exception) -> str:
    if isinstance(error, FileExistsError):
        return "출력 폴더가 이미 있습니다. 다른 이름이나 위치를 선택해 주세요."
    if isinstance(error, FileNotFoundError):
        if "Original disc file missing:" in str(error):
            return "일본판 원본 CUE와 14개 BIN 파일이 모두 같은 폴더에 있어야 합니다.\n" + str(error)
        return "필요한 파일을 찾을 수 없습니다.\n" + str(error)
    detail = str(error)
    if "Original Track 02 SHA-256" in detail or "expects the original Japanese Track 02" in detail:
        return "선택한 디스크는 이 패치가 지원하는 일본판 원본과 다릅니다. Redump 14트랙 원본을 확인해 주세요."
    if "Output must not be inside" in detail:
        return "출력 폴더는 원본 디스크 폴더 밖에 지정해 주세요."
    if isinstance(error, PermissionError):
        return "파일 접근이 거부됐습니다. 다른 프로그램에서 디스크 파일을 사용 중인지, 저장 위치에 쓸 수 있는지 확인해 주세요."
    return "패치를 완료하지 못했습니다.\n" + detail


class PatchWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("팀 이노센트 한국어 패치 v0.735")
        self.root.geometry("790x580")
        self.root.minsize(710, 530)
        self.root.configure(bg=BG)
        self.messages: queue.Queue[tuple] = queue.Queue()
        self.cancelled = threading.Event()
        self.working = False
        self.close_after_work = False
        self.result_cue: Path | None = None
        self.source_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.stage_var = tk.StringVar(value="준비됨 · 원본 CUE 파일을 선택해 주세요")
        self.percent_var = tk.StringVar(value="0%")
        self.progress_var = tk.DoubleVar(value=0)
        self._build()
        self.root.update_idletasks()
        available_height = max(550, self.root.winfo_screenheight() - 100)
        initial_height = min(max(620, self.root.winfo_reqheight() + 20), available_height)
        self.root.geometry(f"790x{initial_height}")
        self.root.deiconify()
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.root.after(100, self._drain_messages)

    def _build(self) -> None:
        title = tk.Frame(self.root, bg=INK, padx=28, pady=23)
        title.pack(fill="x")
        tk.Label(title, text="TEAM INNOCENT", bg=INK, fg="#b9dafd",
                 font=("Malgun Gothic", 10, "bold")).pack(anchor="w")
        tk.Label(title, text="팀 이노센트 한국어 패치", bg=INK, fg=WHITE,
                 font=("Malgun Gothic", 19, "bold")).pack(anchor="w", pady=(3, 2))
        tk.Label(title, text="v0.735 테스트 버전  ·  일본판 14트랙 CUE/BIN 전용",
                 bg=INK, fg="#d0dbe9", font=("Malgun Gothic", 10)).pack(anchor="w")

        # Reserve the action row before the flexible log area. Windows DPI
        # scaling can otherwise push the button below the initial window.
        footer = tk.Frame(self.root, bg=BG, padx=28, pady=15)
        footer.pack(side="bottom", fill="x")
        body = tk.Frame(self.root, bg=BG, padx=28, pady=19)
        body.pack(fill="both", expand=True)
        self._field(body, "1  일본판 원본 CUE", self.source_var, "CUE 선택", self._choose_source,
                    "14개 BIN이 같은 폴더에 있어야 합니다.")
        self._field(body, "2  결과를 저장할 새 폴더", self.output_var, "위치 선택", self._choose_output,
                    "원본은 그대로 두고, 새 폴더에 한국어판을 만듭니다.")

        status = tk.Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, padx=17, pady=15)
        status.pack(fill="x", pady=(12, 0))
        line = tk.Frame(status, bg=WHITE)
        line.pack(fill="x")
        tk.Label(line, textvariable=self.stage_var, bg=WHITE, fg=INK,
                 font=("Malgun Gothic", 10, "bold")).pack(side="left")
        tk.Label(line, textvariable=self.percent_var, bg=WHITE, fg=ACCENT,
                 font=("Malgun Gothic", 10, "bold")).pack(side="right")
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Patch.Horizontal.TProgressbar", troughcolor="#e4ebf4",
                        background=ACCENT, thickness=15)
        ttk.Progressbar(status, variable=self.progress_var, maximum=100,
                        style="Patch.Horizontal.TProgressbar").pack(fill="x", pady=(12, 5))
        tk.Label(status, text="원본 검사 → 디스크 복사 → 패치 적용 → 결과 검사",
                 bg=WHITE, fg=MUTED, font=("Malgun Gothic", 9)).pack(anchor="w")

        log_label = tk.Label(body, text="진행 기록", bg=BG, fg=INK,
                             font=("Malgun Gothic", 10, "bold"))
        log_label.pack(anchor="w", pady=(15, 5))
        log_frame = tk.Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        log_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        self.log = tk.Text(log_frame, height=6, wrap="word", yscrollcommand=scrollbar.set,
                           bg=WHITE, fg=MUTED, relief="flat", padx=12, pady=9,
                           font=("Malgun Gothic", 9), state="disabled")
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=self.log.yview)
        self._log("원본 파일은 수정하지 않습니다. 출력 폴더는 검증이 끝난 뒤에만 만들어집니다.")

        buttons = tk.Frame(footer, bg=BG)
        buttons.pack(fill="x")
        self.apply_button = ttk.Button(buttons, text="한국어 패치 적용", command=self._start)
        self.apply_button.pack(side="left", ipadx=17, ipady=7)
        self.cancel_button = ttk.Button(buttons, text="취소", command=self._cancel, state="disabled")
        self.cancel_button.pack(side="left", padx=(9, 0), ipadx=10, ipady=7)
        self.open_button = ttk.Button(buttons, text="완성 폴더 열기", command=self._open_output, state="disabled")
        self.open_button.pack(side="right", ipadx=10, ipady=7)

    def _field(self, parent: tk.Widget, title: str, variable: tk.StringVar,
               button_text: str, command, hint: str) -> None:
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="x", pady=(0, 14))
        tk.Label(frame, text=title, bg=BG, fg=INK,
                 font=("Malgun Gothic", 10, "bold")).pack(anchor="w")
        row = tk.Frame(frame, bg=BG)
        row.pack(fill="x", pady=(6, 2))
        entry = ttk.Entry(row, textvariable=variable, font=("Malgun Gothic", 10))
        entry.pack(side="left", fill="x", expand=True, ipady=5)
        button = ttk.Button(row, text=button_text, command=command)
        button.pack(side="left", padx=(8, 0), ipadx=6, ipady=5)
        tk.Label(frame, text=hint, bg=BG, fg=MUTED,
                 font=("Malgun Gothic", 9)).pack(anchor="w")
        if variable is self.source_var:
            self.source_entry, self.source_button = entry, button
        else:
            self.output_entry, self.output_button = entry, button

    def _choose_source(self) -> None:
        filename = filedialog.askopenfilename(
            parent=self.root, title="일본판 Team Innocent CUE 선택",
            filetypes=[("PC-FX CUE 파일", "*.cue"), ("모든 파일", "*.*")])
        if not filename:
            return
        cue = Path(filename)
        self.source_var.set(str(cue))
        self.output_var.set(str(available_output(cue.parent.parent)))
        self.result_cue = None
        self.open_button.configure(state="disabled")
        self._log(f"원본 선택: {cue}")

    def _choose_output(self) -> None:
        directory = filedialog.askdirectory(parent=self.root, title="결과를 저장할 상위 폴더 선택")
        if directory:
            self.output_var.set(str(available_output(Path(directory))))
            self._log(f"저장 위치 선택: {self.output_var.get()}")

    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _start(self) -> None:
        cue = Path(self.source_var.get().strip().strip('"'))
        output_text = self.output_var.get().strip().strip('"')
        if not self.source_var.get().strip() or not cue.is_file() or cue.name != CUE:
            messagebox.showerror("원본 CUE 확인", "지원하는 일본판 CUE 파일을 선택해 주세요.", parent=self.root)
            return
        if not output_text:
            messagebox.showerror("저장 위치 확인", "결과를 저장할 새 폴더를 지정해 주세요.", parent=self.root)
            return
        output = Path(output_text)
        if output.exists():
            messagebox.showerror("저장 위치 확인", "출력 폴더가 이미 있습니다. 다른 이름을 지정해 주세요.", parent=self.root)
            return
        self.cancelled.clear()
        self.result_cue = None
        self.working = True
        self.apply_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.open_button.configure(state="disabled")
        self.source_entry.configure(state="disabled")
        self.output_entry.configure(state="disabled")
        self.source_button.configure(state="disabled")
        self.output_button.configure(state="disabled")
        self.progress_var.set(0)
        self.percent_var.set("0%")
        self._log("원본 검사를 시작합니다.")
        threading.Thread(target=self._worker, args=(cue.parent, output), daemon=True).start()

    def _worker(self, source: Path, output: Path) -> None:
        last = (-1, -1)
        def progress(step: int, label: str, fraction: float) -> None:
            nonlocal last
            current = (step, round(fraction * 100))
            if current != last:
                self.messages.put(("progress", step, label, fraction))
                last = current
        try:
            cue = apply_patch(source, output, progress, self.cancelled.is_set)
            self.messages.put(("done", cue))
        except PatchCancelled:
            self.messages.put(("cancelled",))
        except Exception as error:
            self.messages.put(("error", error))

    def _drain_messages(self) -> None:
        try:
            while True:
                item = self.messages.get_nowait()
                kind = item[0]
                if kind == "progress":
                    _, step, label, fraction = item
                    if not hasattr(self, "_last_step") or self._last_step != step:
                        self._log(f"{step + 1}/4  {label}")
                        self._last_step = step
                    percent = (step + fraction) * 25
                    self.progress_var.set(percent)
                    self.percent_var.set(f"{percent:.0f}%")
                    self.stage_var.set(f"{step + 1}/4  {label}")
                elif kind == "done":
                    self.result_cue = item[1]
                    self.progress_var.set(100)
                    self.percent_var.set("100%")
                    self.stage_var.set("완료 · 한국어판 디스크가 준비됐습니다")
                    self._log(f"완료: {self.result_cue}")
                    self._finish()
                    self.open_button.configure(state="normal")
                    messagebox.showinfo("패치 완료", "한국어판 디스크를 만들었습니다.\n\n" +
                                        str(self.result_cue), parent=self.root)
                elif kind == "cancelled":
                    self.stage_var.set("취소됨 · 원본 파일은 그대로입니다")
                    self._log("사용자 요청으로 중단했습니다. 임시 파일을 정리했습니다.")
                    self._finish()
                elif kind == "error":
                    error = item[1]
                    self.stage_var.set("실패 · 원본 파일은 그대로입니다")
                    self._log("오류: " + str(error))
                    self._finish()
                    messagebox.showerror("패치 실패", friendly_error(error), parent=self.root)
        except queue.Empty:
            pass
        if self.close_after_work and not self.working:
            self.root.destroy()
        else:
            self.root.after(100, self._drain_messages)

    def _finish(self) -> None:
        self.working = False
        self.apply_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.source_entry.configure(state="normal")
        self.output_entry.configure(state="normal")
        self.source_button.configure(state="normal")
        self.output_button.configure(state="normal")
        if hasattr(self, "_last_step"):
            del self._last_step

    def _cancel(self) -> None:
        if self.working:
            self.cancelled.set()
            self.cancel_button.configure(state="disabled")
            self.stage_var.set("취소 요청 중 · 임시 파일 정리 후 중단합니다")

    def _open_output(self) -> None:
        if self.result_cue and self.result_cue.is_file():
            os.startfile(str(self.result_cue.parent))

    def _close(self) -> None:
        if not self.working:
            self.root.destroy()
            return
        if messagebox.askyesno("패치 진행 중", "패치를 중단하고 창을 닫을까요?\n임시 파일을 정리한 뒤 종료합니다.",
                               parent=self.root):
            self.close_after_work = True
            self._cancel()

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-bundle", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.verify_bundle:
        header, data = read_patch()
        print(f"Patch bundle OK: {header['record_count']} records, {len(data)} bytes")
        return 0
    PatchWindow().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
