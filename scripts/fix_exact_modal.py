import re

admin_path = r"c:\healthCareTokenSystem\dashboards\admin.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

premium_modal_html = """<!-- Edit Profile Modal -->
    <div class="modal-overlay" id="editModal">
        <div class="modal-content premium" style="max-width: 1000px; grid-template-columns: 280px 1fr; background: var(--bg-panel); border-radius: 20px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);">
            <div class="modal-aside" style="background: rgba(15, 23, 42, 0.6); padding: 40px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column;">
                <div style="width: 48px; height: 48px; background: var(--accent-orange); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; color: #fff;">
                    <i data-lucide="building-2"></i>
                </div>
                <h2 style="font-family: 'Outfit'; font-size: 1.5rem; margin-bottom: 12px; color: #fff;">Facility Identity</h2>
                <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.6;">This profile information is what patients see when searching for your hospital.</p>
                <div style="flex: 1;"></div>
                <button class="close-btn" onclick="closeEditModal()" style="align-self: flex-start; margin-top: 40px; color: var(--text-muted); font-weight: 500; font-size: 0.85rem; display: flex; align-items: center; gap: 8px;"><i data-lucide="arrow-left" size="16"></i> Go Back</button>
            </div>

            <div class="modal-body" style="padding: 40px;">
                <form onsubmit="saveHospitalProfile(event)">
                    
                    <div class="form-group" style="margin-bottom: 24px;">
                        <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 12px; display: block; font-weight: 700;">HOSPITAL NAME</label>
                        <input type="text" id="editHospName" required placeholder="ArogyaCare Super Speciality Hospital" style="background: rgba(10, 15, 28, 0.4); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px; color: #fff; width: 100%; font-size: 0.95rem;">
                    </div>

                    <div class="form-group" style="margin-bottom: 24px;">
                        <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 12px; display: block; font-weight: 700;">FACILITY BANNER IMAGE</label>
                        <div class="photo-dropzone" onclick="document.getElementById('fileInput').click()" style="width: 100%; height: 180px; background: rgba(10, 15, 28, 0.4); border: 2px dashed rgba(255,255,255,0.1); border-radius: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; cursor: pointer; position: relative; overflow: hidden; transition: 0.2s;">
                            <i data-lucide="image" style="color: var(--text-muted); width: 32px; height: 32px;" id="dzIcon"></i>
                            <span style="font-size: 0.85rem; font-weight: 500; color: var(--text-muted);" id="dzText">Click to upload photo<br><small style="color: #64748b; font-weight: 400;">Recommended 1200x600px</small></span>
                            <img id="photoPreview" alt="Facility Preview" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: none;">
                            <input type="file" id="fileInput" hidden accept="image/*" onchange="handleFilePreview(event)">
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 24px; position: relative;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin: 0; font-weight: 700;">FACILITY ADDRESS (FREE SEARCH)</label>
                            <button type="button" onclick="toggleMap()" style="background: none; border: none; color: var(--accent-orange); font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 6px; cursor: pointer;"><i data-lucide="crosshair" size="14"></i> Use GPS</button>
                        </div>
                        <div style="position: relative; display: flex; align-items: center;">
                            <i data-lucide="search" size="18" style="position: absolute; left: 16px; color: var(--text-muted);"></i>
                            <input type="text" id="searchAddressInput" placeholder="Search for hospital name or area..." oninput="handleAddressSearch(this.value)" style="background: rgba(10, 15, 28, 0.4); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px 14px 44px; color: #fff; width: 100%; font-size: 0.95rem;">
                            <button type="button" onclick="toggleMap()" style="position: absolute; right: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 6px 10px; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; justify-content: center;"><i data-lucide="map" size="16"></i></button>
                        </div>
                        <div id="searchResults" class="search-results hidden" style="position: absolute; top: 100%; left: 0; right: 0; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 12px; max-height: 200px; overflow-y: auto; z-index: 1000; margin-top: 4px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);"></div>
                    </div>

                    <div id="mapPicker" class="hidden" style="width: 100%; height: 200px; border-radius: 12px; margin-bottom: 24px; border: 1px solid var(--border-color);"></div>
                    
                    <div id="confirmedAddressCard" class="hidden" style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); padding: 14px 16px; border-radius: 12px; display: flex; gap: 12px; align-items: flex-start; margin-bottom: 24px;">
                        <i data-lucide="check-circle-2" style="color: var(--success); flex-shrink: 0; margin-top: 2px;"></i>
                        <div>
                            <p style="margin: 0; font-size: 0.75rem; font-weight: 700; color: var(--success); letter-spacing: 0.05em; margin-bottom: 4px;">VERIFIED LOCATION</p>
                            <p id="confirmedAddressText" style="margin: 0; font-size: 0.85rem; color: #e2e8f0; line-height: 1.4;">No address selected</p>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
                        <div class="form-group">
                            <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 12px; display: block; font-weight: 700;">PRIMARY SPECIALIZATION</label>
                            <select id="editHospSpec" style="width: 100%; background: rgba(10, 15, 28, 0.4); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px; color: #fff; font-size: 0.95rem; appearance: none;">
                                <option style="background: var(--bg-panel);" value="General Medicine">General Medicine</option>
                                <option style="background: var(--bg-panel);" value="Cardiology">Cardiology (Heart)</option>
                                <option style="background: var(--bg-panel);" value="Nephrology">Nephrology (Kidney)</option>
                                <option style="background: var(--bg-panel);" value="Orthopedics">Orthopedics</option>
                                <option style="background: var(--bg-panel);" value="Neurology">Neurology</option>
                                <option style="background: var(--bg-panel);" value="Pediatrics">Pediatrics</option>
                                <option style="background: var(--bg-panel);" value="Multi-Speciality">Multi-Speciality</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 12px; display: block; font-weight: 700;">STAFF COUNT</label>
                            <input type="number" id="editHospDocs" min="0" placeholder="e.g. 50" style="background: rgba(10, 15, 28, 0.4); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px; color: #fff; width: 100%; font-size: 0.95rem;">
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 32px;">
                        <label style="font-size: 0.75rem; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 12px; display: block; font-weight: 700;">ABOUT THE FACILITY</label>
                        <textarea id="editHospDesc" rows="4" placeholder="Describe your unique medical services..." required style="background: rgba(10, 15, 28, 0.4); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px; color: #fff; width: 100%; font-size: 0.95rem; resize: vertical;"></textarea>
                    </div>

                    <button type="submit" class="btn-edit" style="width: 100%; justify-content: center; padding: 16px; font-size: 1rem; border-radius: 12px;">Save Profile Updates</button>
                </form>
            </div>
        </div>
    </div>

    <script src="../js/services/supabase.js">"""

content = re.sub(r'<!-- Edit Profile Modal -->.*?<script src="\.\./js/services/supabase\.js">', premium_modal_html, content, flags=re.DOTALL)

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modal replaced with exact visual replica.")
