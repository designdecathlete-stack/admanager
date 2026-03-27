file_path = "c:/Users/kanat/.gemini/antigravity/scratch/admanager/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False

repl_app = '''            const handleSaveNewClient = async (newClient) => {
                if (!supabase) {
                    setClients(prev => [newClient, ...prev]);
                    setView("clientList");
                    return;
                }
                setIsLoading(true);
                try {
                    const dbData = {
                        name: newClient.name,
                        assignee: newClient.assignee,
                        plan: newClient.plan,
                        contract_date: newClient.contractDate || null,
                        status: 'paused',
                        budget: 0,
                        target_cpa: 0,
                        limit_cpa: 0
                    };
                    const { data, error } = await supabase.from('clients').insert([dbData]).select('*');
                    if (error) throw error;
                    if (data && data.length > 0) {
                        const c = data[0];
                        const mapped = {
                            id: c.id,
                            name: c.name,
                            assignee: c.assignee,
                            status: c.status,
                            budget: c.budget,
                            targetCpa: c.target_cpa,
                            limitCpa: c.limit_cpa,
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
                            spend: 0, prevSpend: 0, cvs: 0, prevCvs: 0, cpa: 0, clicks: 0, impressions: 0, historyCvs: []
                        };
                        setClients(prev => [mapped, ...prev]);
                    }
                } catch(e) {
                    console.error("Error saving new client", e);
                } finally {
                    setIsLoading(false);
                    setView("clientList");
                }
            };
            
            const handleUpdateClient = async (updatedClient) => {
                setClients(prev => prev.map(c => c.id === updatedClient.id ? updatedClient : c));
                setSelectedClient(prev => prev && prev.id === updatedClient.id ? updatedClient : prev);
                
                if (!supabase || ("" + updatedClient.id).startsWith("cl")) return;
                
                try {
                    const info = updatedClient.info || {};
                    const updateData = {
                        name: updatedClient.name,
                        assignee: info.assignee !== undefined ? info.assignee : updatedClient.assignee,
                        status: updatedClient.status,
                        budget: updatedClient.budget,
                        target_cpa: updatedClient.targetCpa,
                        limit_cpa: updatedClient.limitCpa,
                        representative_name: info.clientContact !== undefined ? info.clientContact : updatedClient.representativeName,
                        business_details: info.businessDetails !== undefined ? info.businessDetails : updatedClient.businessDetails,
                        main_services: info.services !== undefined ? info.services : updatedClient.mainServices,
                        url_website: info.websiteUrl !== undefined ? info.websiteUrl : updatedClient.urlWebsite,
                        url_hotpepper: info.hotpepperUrl !== undefined ? info.hotpepperUrl : updatedClient.urlHotpepper,
                        url_line: info.lineUrl !== undefined ? info.lineUrl : updatedClient.urlLine,
                        url_instagram: info.instagramUrl !== undefined ? info.instagramUrl : updatedClient.urlInstagram,
                        pixel_id: info.pixelId !== undefined ? info.pixelId : updatedClient.pixelId,
                        url_drive: info.assetUrl !== undefined ? info.assetUrl : updatedClient.urlDrive,
                        url_guideline: info.guidelineUrl !== undefined ? info.guidelineUrl : updatedClient.urlGuideline
                    };
                    await supabase.from('clients').update(updateData).eq('id', updatedClient.id);
                } catch(e) {
                    console.error("Error updating client", e);
                }
            };
'''

repl_log = '''            const handleAddLog = async (e) => {
                e.preventDefault();
                const now = new Date();
                const d = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
                
                const logEntry = {
                    client_id: client.id,
                    action_date: d,
                    assignee: logUser,
                    category_main: logCategory,
                    category_sub: logSubCategory,
                    value_before: logBefore,
                    value_after: logAfter,
                    memo: newLog || "(メモなし)"
                };
                
                if (supabase && !("" + client.id).startsWith("cl")) {
                    try {
                        const { data, error } = await supabase.from('change_logs').insert([logEntry]).select('*');
                        if (error) throw error;
                        if (data && data.length > 0) {
                            const dRecord = data[0];
                            setDbHistoryLogs([{
                                id: dRecord.id,
                                date: dRecord.action_date,
                                user: dRecord.assignee || '不明',
                                action: `${dRecord.category_main}: ${dRecord.category_sub}`,
                                detail: dRecord.memo,
                                before: dRecord.value_before,
                                after: dRecord.value_after
                            }, ...dbHistoryLogs]);
                        }
                    } catch(err) {
                        console.error("Error saving log", err);
                    }
                } else {
                    setHistoryLogs([{ id: Date.now(), date: d, user: logUser, action: `${logCategory}: ${logSubCategory}`, detail: newLog || "(メモなし)", before: logBefore, after: logAfter }, ...historyLogs]);
                }
                
                setNewLog("");
                setLogBefore("");
                setLogAfter("");
            };
'''

repl_minute = '''            const handleAddMinute = async (e) => {
                e.preventDefault();
                if (!newMinuteTitle || !newMinuteDate || !newMinuteText) return;
                
                const noteEntry = {
                    client_id: client.id,
                    meeting_date: newMinuteDate,
                    title: newMinuteTitle,
                    url: newMinuteUrl,
                    summary: newMinuteText
                };
                
                if (supabase && !("" + client.id).startsWith("cl")) {
                    try {
                        const { data, error } = await supabase.from('meeting_notes').insert([noteEntry]).select('*');
                        if (error) throw error;
                        if (data && data.length > 0) {
                            const nRecord = data[0];
                            setDbMinutesLogs([{
                                id: nRecord.id,
                                date: nRecord.meeting_date,
                                user: 'ログインユーザー',
                                title: nRecord.title,
                                detail: nRecord.summary,
                                url: nRecord.url
                            }, ...dbMinutesLogs]);
                        }
                    } catch(err) {
                        console.error("Error saving minute", err);
                    }
                } else {
                    setMinutesLogs([{ id: Date.now(), date: newMinuteDate, user: "ログインユーザー", title: newMinuteTitle, detail: newMinuteText, url: newMinuteUrl }, ...minutesLogs]);
                }

                setNewMinuteDate(getTodayStr());
                setNewMinuteTitle("");
                setNewMinuteText("");
                setNewMinuteUrl("");
            };
'''

i = 0
while i < len(lines):
    line = lines[i]
    
    # 1. handleSaveNewClient
    if "const handleSaveNewClient = (newClient) => {" in line:
        new_lines.append(repl_app)
        i += 4
        continue
        
    # 2. handleAddLog
    if "const handleAddLog = (e) => {" in line:
        new_lines.append(repl_log)
        i += 9
        continue

    # 3. handleAddMinute
    if "const handleAddMinute = (e) => {" in line:
        new_lines.append(repl_minute)
        i += 8
        continue

    # 4. inline onUpdateClient
    if "onUpdateClient={(updated) => { setClients(prev => prev.map(c => c.id === updated.id ? updated : c)); setSelectedClient(updated); }}" in line:
        new_lines.append(line.replace("onUpdateClient={(updated) => { setClients(prev => prev.map(c => c.id === updated.id ? updated : c)); setSelectedClient(updated); }}", "onUpdateClient={handleUpdateClient}"))
        i += 1
        continue

    new_lines.append(line)
    i += 1

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Line-based patch applied")
