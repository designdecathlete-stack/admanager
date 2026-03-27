import sys

filepath = r"c:\Users\kanat\.gemini\antigravity\scratch\admanager\index.html"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.read().split('\n')

start_idx = -1
end_idx = -1

# search for start
for i, line in enumerate(lines):
    if '<div className="space-y-4">' in line and 'minutesLogs.map' in lines[i+1]:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find start index")
    sys.exit(1)

# search for end
for i in range(start_idx, len(lines)):
    if '</div>' in lines[i] and '))} ' in lines[i-1] or '{minutesLogs.map(log => (' in lines[i-2] or ('</Card>' in lines[i-1] and '))} ' in lines[i-1]):
        pass
    
# simpler end search: just look for the first </div> after </Card> ))}
for i in range(start_idx, len(lines)):
    if '</Card>' in lines[i]:
        if '))} ' in lines[i+1] or '))}' in lines[i+1]:
            if '</div>' in lines[i+2]:
                end_idx = i + 2
                break

if end_idx == -1:
    # let's try a different approach, just exactly matching the array indices we know from view_file:
    # We viewed lines 980 to 1040, then 1025 to 1080.
    # start is 1002 (index 1001). end is 1060 (index 1059).
    pass

# Safe slice replacement using line index limits
for i, line in enumerate(lines):
    if line.strip() == '<div className="space-y-4">' and lines[i+1].strip() == '{minutesLogs.map(log => (':
        start_idx = i
        break

for i in range(start_idx, len(lines)):
    if lines[i].strip() == '</div>' and lines[i-1].strip() == '))}':
        end_idx = i
        break

if end_idx == -1 or start_idx == -1:
    print(f"FAILED to find slice. start={start_idx}, end={end_idx}")
    sys.exit(1)

replacement = """                            <div className="relative pl-4 border-l-2 border-slate-200/60 ml-4 pb-8 space-y-12 mt-8">
                                {(() => {
                                    const grouped = minutesLogs.reduce((acc, log) => {
                                        if(!acc[log.date]) acc[log.date] = [];
                                        acc[log.date].push(log);
                                        return acc;
                                    }, {});
                                    const sortedDates = Object.keys(grouped).sort((a,b) => new Date(b) - new Date(a));
                                    
                                    return sortedDates.map(date => {
                                        const [y, m, d] = date.split('-');
                                        const formattedDate = `${y}年${parseInt(m)}月${parseInt(d)}日`;
                                        
                                        return (
                                            <div key={date} className="relative">
                                                <div className="flex items-center gap-4 relative z-10 -ml-[15px]">
                                                    <div className="w-8 h-8 rounded-full bg-slate-50 flex items-center justify-center border border-slate-200 shadow-sm text-slate-500">
                                                        <Icon name="Calendar" size={14} />
                                                    </div>
                                                    <h4 className="font-bold text-slate-800 tracking-tight">{formattedDate}</h4>
                                                </div>
                                                
                                                <div className="space-y-6 mt-6 ml-[15px] pl-8">
                                                    {grouped[date].map(log => (
                                                        <div key={log.id} className="relative border border-slate-100 bg-white rounded-lg p-5 shadow-[0_2px_8px_-4px_rgba(0,0,0,0.1)] hover:shadow-md transition-shadow group">
                                                            <div className="absolute -left-[37px] top-6 w-[9px] h-[9px] rounded-full bg-primary/80 ring-4 ring-white shadow-sm" />
                                                            {editMinuteId === log.id ? (
                                                                <div className="space-y-4">
                                                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                        <div>
                                                                            <label className="text-xs font-semibold text-slate-500 mb-1 block">打ち合わせ日</label>
                                                                            <input type="date" value={editMinuteForm.date} onChange={e => setEditMinuteForm({...editMinuteForm, date: e.target.value})} className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:border-primary" />
                                                                        </div>
                                                                        <div>
                                                                            <label className="text-xs font-semibold text-slate-500 mb-1 block">タイトル</label>
                                                                            <input type="text" value={editMinuteForm.title} onChange={e => setEditMinuteForm({...editMinuteForm, title: e.target.value})} className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:border-primary" />
                                                                        </div>
                                                                    </div>
                                                                    <div>
                                                                        <label className="text-xs font-semibold text-slate-500 mb-1 block">詳細議事録URL</label>
                                                                        <input type="url" value={editMinuteForm.url} onChange={e => setEditMinuteForm({...editMinuteForm, url: e.target.value})} className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:border-primary" placeholder="任意" />
                                                                    </div>
                                                                    <div>
                                                                        <label className="text-xs font-semibold text-slate-500 mb-1 block">要約・決定事項</label>
                                                                        <textarea value={editMinuteForm.detail} onChange={e => setEditMinuteForm({...editMinuteForm, detail: e.target.value})} className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:border-primary min-h-[100px]" />
                                                                    </div>
                                                                    <div className="flex justify-end gap-2 pt-2">
                                                                        <button onClick={() => setEditMinuteId(null)} className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 bg-slate-100 rounded-md transition-colors">キャンセル</button>
                                                                        <button onClick={handleSaveMinute} className="px-4 py-2 text-sm font-medium text-white bg-primary hover:bg-primary/90 rounded-md flex items-center gap-2 transition-colors"><Icon name="Save" size={16}/> 保存</button>
                                                                    </div>
                                                                </div>
                                                            ) : (
                                                                <>
                                                                    <div className="absolute right-3 top-3 opacity-80 hover:opacity-100 transition-opacity flex gap-2 z-10">
                                                                        <button onClick={() => { setEditMinuteId(log.id); setEditMinuteForm({...log}); }} className="px-3 py-1.5 text-[11px] font-bold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Edit3" size={14} /> 編集</button>
                                                                        <button onClick={() => handleDeleteMinute(log.id)} className="px-3 py-1.5 text-[11px] font-bold text-rose-600 hover:text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200/60 shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Trash2" size={14} /> 削除</button>
                                                                    </div>
                                                                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4 border-b border-slate-100 pb-4 pr-32">
                                                                        <h4 className="text-lg font-bold text-slate-900 flex items-center gap-2 max-w-full">
                                                                            <Icon name="BookOpen" size={18} className="text-slate-400 shrink-0" />
                                                                            <span className="truncate">{log.title}</span>
                                                                        </h4>
                                                                        <div className="flex items-center gap-3 text-xs text-slate-500 shrink-0">
                                                                            {/* Date is removed from here since it's the timeline node */}
                                                                            <span className="flex items-center gap-1"><Icon name="User" size={12} /> {log.user}</span>
                                                                        </div>
                                                                    </div>
                                                                    <div className="text-sm text-slate-800 leading-[1.8] whitespace-pre-wrap break-words bg-slate-50/50 p-4 rounded-md border border-slate-100">
                                                                        {log.detail}
                                                                    </div>
                                                                    {log.url && (
                                                                        <div className="mt-4 pt-3 border-t border-slate-100 flex justify-end">
                                                                            <a href={log.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary bg-primary/5 hover:bg-primary/10 px-4 py-2 rounded-full transition-colors border border-primary/10">
                                                                                <Icon name="ExternalLink" size={14} /> 詳細な議事録を開く
                                                                            </a>
                                                                        </div>
                                                                    )}
                                                                </>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        );
                                    });
                                })()}
                            </div>"""

new_lines = lines[:start_idx] + replacement.split('\n') + lines[end_idx+1:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write('\n'.join(new_lines))

print(f"SUCCESS. Replaced lines {start_idx} to {end_idx}.")
