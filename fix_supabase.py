import re

file_path = "c:/Users/kanat/.gemini/antigravity/scratch/admanager/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Supabase script
text = text.replace(
    '<script src="https://unpkg.com/lucide@latest"></script>',
    '<script src="https://unpkg.com/lucide@latest"></script>\n    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
)

# 2. Add Supabase client
text = text.replace(
    'const { useState, useEffect, useMemo } = React;',
    'const { useState, useEffect, useMemo, useCallback } = React;\n\n        const SUPABASE_URL = "YOUR_SUPABASE_URL_HERE";\n        const SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY_HERE";\n        const supabase = window.supabase && SUPABASE_URL !== "YOUR_SUPABASE_URL_HERE" ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;'
)

# 3. Rewrite App
app_old = '''        const App = () => {
            const [clients, setClients] = useState(initialClientsMock);
            const [view, setView] = useState("clientList");
            const [selectedClient, setSelectedClient] = useState(null);'''

app_new = '''        const App = () => {
            const [clients, setClients] = useState([]);
            const [isLoading, setIsLoading] = useState(true);
            const [view, setView] = useState("clientList");
            const [selectedClient, setSelectedClient] = useState(null);

            useEffect(() => {
                const fetchClients = async () => {
                    if (!supabase) {
                        setClients(initialClientsMock);
                        setIsLoading(false);
                        return;
                    }
                    try {
                        const { data, error } = await supabase.from('clients').select('*');
                        if (error) throw error;
                        
                        const mapped = data.map(c => ({
                            id: c.id,
                            name: c.name,
                            assignee: c.assignee,
                            status: c.status || 'active',
                            budget: c.budget || 0,
                            targetCpa: c.target_cpa || 0,
                            limitCpa: c.limit_cpa || 0,
                            plan: c.plan,
                            contractDate: c.contract_date,
                            representativeName: c.representative_name,
                            businessDetails: c.business_details,
                            mainServices: c.main_services,
                            urlWebsite: c.url_website,
                            urlHotpepper: c.url_hotpepper,
                            urlLine: c.url_line,
                            urlInstagram: c.url_instagram,
                            pixelId: c.pixel_id,
                            urlDrive: c.url_drive,
                            urlGuideline: c.url_guideline,
                            // defaults for list view if no metrics yet
                            spend: 0, prevSpend: 0, cvs: 0, prevCvs: 0, cpa: 0, clicks: 0, impressions: 0, historyCvs: []
                        }));
                        setClients(mapped.length > 0 ? mapped : initialClientsMock);
                    } catch (err) {
                        console.error('Error', err);
                        setClients(initialClientsMock);
                    } finally {
                        setIsLoading(false);
                    }
                };
                fetchClients();
            }, []);'''
            
text = text.replace(app_old, app_new)

# 4. Handle rendering loading state if needed, but for simplicity let React handle empty array

# 5. DashboardDetail fetching
detail_old = '''        const DashboardDetail = ({ client, onBack, onUpdateClient }) => {
            const data = useMemo(() => generateClientData(client), [client]);
            const [expandedRows, setExpandedRows] = useState(new Set([`${client.id}-c1`, `${client.id}-as1`]));
            const [activeTab, setActiveTab] = useState("dashboard"); // dashboard, history, minutes, info
            const [activeInfoTab, setActiveInfoTab] = useState("basic"); // basic, links, ad, creative
            const [dateRange, setDateRange] = useState("this_month");'''

detail_new = '''        const DashboardDetail = ({ client, onBack, onUpdateClient }) => {
            const [data, setData] = useState(useMemo(() => generateClientData(client), [client]));
            const [expandedRows, setExpandedRows] = useState(new Set([`${client.id}-c1`, `${client.id}-as1`]));
            const [activeTab, setActiveTab] = useState("dashboard");
            const [activeInfoTab, setActiveInfoTab] = useState("basic");
            const [dateRange, setDateRange] = useState("this_month");

            // Supabase states
            const [dbHistoryLogs, setDbHistoryLogs] = useState([]);
            const [dbMinutesLogs, setDbMinutesLogs] = useState([]);

            useEffect(() => {
                const loadDetails = async () => {
                    if(!supabase) return;
                    try {
                        // ad_metrics (if you want to fetch and replace data here)
                        // const resAd = await supabase.from('ad_metrics').select('*').eq('client_id', client.id);
                        
                        // change_logs
                        const resLogs = await supabase.from('change_logs').select('*').eq('client_id', client.id).order('action_date', { ascending: false });
                        if(resLogs.data) {
                            setDbHistoryLogs(resLogs.data.map(d => ({
                                id: d.id,
                                date: d.action_date,
                                user: d.assignee || '不明',
                                action: `${d.category_main}: ${d.category_sub}`,
                                detail: d.memo,
                                before: d.value_before,
                                after: d.value_after
                            })));
                        }

                        // meeting_notes
                        const resNotes = await supabase.from('meeting_notes').select('*').eq('client_id', client.id).order('meeting_date', { ascending: false });
                        if(resNotes.data) {
                            setDbMinutesLogs(resNotes.data.map(d => ({
                                id: d.id,
                                date: d.meeting_date,
                                user: '不明', // Or add assignee to table
                                title: d.title,
                                detail: d.summary,
                                url: d.url
                            })));
                        }
                    } catch(e) { console.error('Error loading details', e); }
                };
                loadDetails();
            }, [client.id]);'''

text = text.replace(detail_old, detail_new)

# 6. Replace `historyLogs` with `dbHistoryLogs.length > 0 ? dbHistoryLogs : historyLogs` 
# Actually, let's just use `const currentHistory = supabase ? dbHistoryLogs : historyLogs;`
text = text.replace(
    'const filtered = historyLogs.filter(log => {',
    'const currentHistory = supabase ? dbHistoryLogs : historyLogs;\n                                    const filtered = currentHistory.filter(log => {'
)

text = text.replace(
    'const grouped = minutesLogs.reduce((acc, log) => {',
    'const currentMinutes = supabase ? dbMinutesLogs : minutesLogs;\n                                    const grouped = currentMinutes.reduce((acc, log) => {'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("done")
