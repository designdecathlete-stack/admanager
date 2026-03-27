import sys

filepath = r"c:\Users\kanat\.gemini\antigravity\scratch\admanager\index.html"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the history log card rendering
target_history = """                                                                            <div className="absolute -left-[37px] top-6 w-[9px] h-[9px] rounded-full bg-primary/80 ring-4 ring-white shadow-sm" />
                                                                            
                                                                            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-3">"""

replacement_history = """                                                                            <div className="absolute -left-[37px] top-6 w-[9px] h-[9px] rounded-full bg-primary/80 ring-4 ring-white shadow-sm" />

                                                                            {editHistoryId === log.id ? (
                                                                                <div className="space-y-3 mt-4">
                                                                                    <textarea autoFocus value={editHistoryForm.detail} onChange={e => setEditHistoryForm({...editHistoryForm, detail: e.target.value})} className="w-full p-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/20 bg-slate-50 focus:bg-white resize-y min-h-[60px]" placeholder="具体的な変更メモ (任意)"/>
                                                                                    <div className="flex gap-2 text-sm">
                                                                                        <input type="text" value={editHistoryForm.before} onChange={e => setEditHistoryForm({...editHistoryForm, before: e.target.value})} className="flex-1 p-2 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/20 bg-slate-50 focus:bg-white" placeholder="変更前 (任意)"/>
                                                                                        <input type="text" value={editHistoryForm.after} onChange={e => setEditHistoryForm({...editHistoryForm, after: e.target.value})} className="flex-1 p-2 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/20 bg-slate-50 focus:bg-white" placeholder="変更後 (任意)"/>
                                                                                    </div>
                                                                                    <div className="flex justify-end gap-2 pt-2">
                                                                                        <button onClick={() => setEditHistoryId(null)} className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-200 bg-slate-100 rounded-md transition-colors">キャンセル</button>
                                                                                        <button onClick={handleSaveHistory} className="px-4 py-1.5 text-xs font-medium text-white bg-primary hover:bg-primary/90 rounded-md flex items-center gap-1.5 shadow-sm transition-colors"><Icon name="Save" size={14}/> 保存</button>
                                                                                    </div>
                                                                                </div>
                                                                            ) : (
                                                                                <>
                                                                                    <div className="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                                                                                        <button onClick={() => { setEditHistoryId(log.id); setEditHistoryForm({...log}); }} className="px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-primary hover:bg-primary/5 border border-slate-200 hover:border-primary/30 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Edit3" size={12} /> 編集</button>
                                                                                        <button onClick={() => handleDeleteHistory(log.id)} className="px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 border border-slate-200 hover:border-red-300 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Trash2" size={12} /> 削除</button>
                                                                                    </div>
                                                                            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-3 pr-20">"""


target_history_end = """                                                                                    {log.detail && <div className="p-3.5"><p>{log.detail}</p></div>}
                                                                                </div>
                                                                            )}
                                                                        </div>
                                                                    );"""

replacement_history_end = """                                                                                    {log.detail && <div className="p-3.5"><p>{log.detail}</p></div>}
                                                                                </div>
                                                                            )}
                                                                                </>
                                                                            )}
                                                                        </div>
                                                                    );"""


if target_history in text:
    text = text.replace(target_history, replacement_history)
    text = text.replace(target_history_end, replacement_history_end)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: History patched.")
else:
    print("FAILED: target_history not found...")
    # debug
    print("Current text snippet near line 864:")
    lines = text.split("\\n")
    for i, line in enumerate(lines[860:870]):
        print(f"[{860+i}] {repr(line)}")
