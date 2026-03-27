import sys

filepath = r"c:\Users\kanat\.gemini\antigravity\scratch\admanager\index.html"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Replace Minutes Edit button
text = text.replace(
    'className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:text-primary hover:bg-primary/5 border border-slate-200 hover:border-primary/30 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Edit3" size={14} /> 編集</button>',
    'className="px-3 py-1.5 text-[11px] font-bold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Edit3" size={14} /> 編集</button>'
)

# Replace Minutes Delete button
text = text.replace(
    'className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 border border-slate-200 hover:border-red-300 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Trash2" size={14} /> 削除</button>',
    'className="px-3 py-1.5 text-[11px] font-bold text-rose-600 hover:text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200/60 shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Trash2" size={14} /> 削除</button>'
)

# Replace History Edit button
text = text.replace(
    'className="px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-primary hover:bg-primary/5 border border-slate-200 hover:border-primary/30 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Edit3" size={12} /> 編集</button>',
    'className="px-3 py-1 text-[11px] font-bold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 shadow-sm rounded-md flex items-center gap-1 transition-all"><Icon name="Edit3" size={12} /> 編集</button>'
)

# Replace History Delete button
text = text.replace(
    'className="px-2.5 py-1 text-xs font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 border border-slate-200 hover:border-red-300 bg-white shadow-sm rounded-md flex items-center gap-1.5 transition-all"><Icon name="Trash2" size={12} /> 削除</button>',
    'className="px-3 py-1 text-[11px] font-bold text-rose-600 hover:text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200/60 shadow-sm rounded-md flex items-center gap-1 transition-all"><Icon name="Trash2" size={12} /> 削除</button>'
)

# Make buttons visible without hover so user knows they can edit/delete easily
text = text.replace(
    'className="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">',
    'className="absolute right-3 top-3 opacity-80 hover:opacity-100 transition-opacity flex gap-2 z-10">'
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)
print("SUCCESS: Colors patched.")
