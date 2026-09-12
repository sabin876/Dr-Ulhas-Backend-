from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape
import json

class ListStringWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - ListStringWidget */
        #cms-list-{id_str} {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        }}
        .cms-widget-container {{
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }}
        .cms-card {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #1e293b !important;
        }}
        .cms-card-title {{
            color: #0f172a !important;
        }}
        .cms-input-field {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }}
        .cms-input-field::placeholder {{
            color: #94a3b8 !important;
        }}
        .cms-form-box {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }}
        
        /* Dark Mode overrides with elevated specificity */
        html.dark .cms-widget-container,
        body.dark .cms-widget-container,
        .dark .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark .cms-card,
        body.dark .cms-card,
        .dark .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark .cms-card-title,
        body.dark .cms-card-title,
        .dark .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field,
        body.dark .cms-input-field,
        .dark .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field::placeholder,
        body.dark .cms-input-field::placeholder,
        .dark .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark .cms-form-box,
        body.dark .cms-form-box,
        .dark .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        </style>

        <div id="cms-list-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newItem: '',
                 addItem() {{
                     if (this.newItem.trim()) {{
                         this.items.push(this.newItem.trim());
                         this.newItem = '';
                     }}
                 }},
                 removeItem(idx) {{
                     this.items.splice(idx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-3 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- List of items -->
            <div class="space-y-2 max-h-64 overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card flex items-center justify-between gap-3 p-3 border rounded-xl shadow-sm hover:border-slate-350 transition-colors">
                        <span class="cms-card-title text-xs font-medium" x-text="item"></span>
                        <button type="button" class="text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeItem(idx)">
                            <span class="material-symbols-outlined align-middle" style="font-size: 18px;">delete</span>
                        </button>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No items added yet.</p>
                </div>
            </div>
            
            <!-- Add Item Input Form -->
            <div class="cms-form-box flex gap-2 mt-4 p-2 border rounded-xl shadow-sm">
                <input type="text" x-model="newItem" @keydown.enter.prevent="addItem()" placeholder="Add new item..." 
                       class="cms-input-field flex-1 text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                <button type="button" @click="addItem()" 
                        class="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add
                </button>
            </div>
        </div>
        """
        return mark_safe(html)

class ConditionsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - ConditionsWidget */
        #cms-cond-{id_str} {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        }}
        .cms-widget-container {{
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }}
        .cms-card {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #1e293b !important;
        }}
        .cms-card-title {{
            color: #0f172a !important;
        }}
        .cms-card-desc, .cms-card-desc * {{
            color: #475569 !important;
        }}
        .cms-input-field {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }}
        .cms-input-field::placeholder {{
            color: #94a3b8 !important;
        }}
        .cms-form-box {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }}
        
        /* Dark Mode overrides with elevated specificity */
        html.dark .cms-widget-container,
        body.dark .cms-widget-container,
        .dark .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark .cms-card,
        body.dark .cms-card,
        .dark .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark .cms-card-title,
        body.dark .cms-card-title,
        .dark .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark .cms-card-desc,
        html.dark .cms-card-desc *,
        body.dark .cms-card-desc,
        body.dark .cms-card-desc *,
        .dark .cms-card-desc,
        .dark .cms-card-desc * {{
            color: #94a3b8 !important;
        }}
        html.dark .cms-input-field,
        body.dark .cms-input-field,
        .dark .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field::placeholder,
        body.dark .cms-input-field::placeholder,
        .dark .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark .cms-form-box,
        body.dark .cms-form-box,
        .dark .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        /* Specific overrides for Unfold's dark mode styling in labels */
        html.dark .cms-label,
        body.dark .cms-label,
        .dark .cms-label {{
            color: #94a3b8 !important;
        }}
        </style>

        <div id="cms-cond-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newTitle: '',
                 newIcon: '',
                 newDesc: '',
                 addItem() {{
                     let desc = this.newDesc.trim();
                     if (this.newTitle.trim() && desc) {{
                         this.items.push({{
                             id: this.items.length + 1,
                             title: this.newTitle.trim(),
                             description: desc,
                             icon: this.newIcon.trim() || `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' width='22' height='22'><path d='M5 12h14M12 5l7 7-7 7' /></svg>`
                         }});
                         this.newTitle = '';
                         this.newIcon = '';
                         this.newDesc = '';
                     }}
                 }},
                 removeItem(idx) {{
                     this.items.splice(idx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-3 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- List of items -->
            <div class="space-y-3 max-h-80 overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-3 border rounded-xl shadow-sm relative space-y-1 hover:border-slate-350 transition-colors">
                        <button type="button" class="absolute top-2 right-2 text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeItem(idx)">
                            <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                        </button>
                        <p class="cms-card-title text-xs font-semibold pr-6 leading-normal" x-text="item.title"></p>
                        <div class="cms-card-desc text-[10px] leading-relaxed pt-1.5 border-t border-slate-50 mt-1" x-html="item.description"></div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No conditions added yet.</p>
                </div>
            </div>
            
            <!-- Add Item Input Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add Condition Card</h4>
                <div class="grid sm:grid-cols-2 gap-3">
                    <input type="text" x-model="newTitle" placeholder="Condition Title (e.g. Back pain)" 
                           class="cms-input-field text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                    <input type="text" x-model="newIcon" placeholder="SVG Icon Code (Optional)" 
                           class="cms-input-field text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 font-mono transition-colors" />
                </div>
                
                <div class="space-y-1">
                    <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Card Description</label>
                    <textarea id="cond-desc-{id_str}" x-model="newDesc" rows="2" placeholder="Condition Description..." 
                              class="cms-input-field w-full text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors"></textarea>
                </div>

                <button type="button" @click="addItem()" 
                        class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add Condition Card
                </button>
            </div>
        </div>
        """
        return mark_safe(html)

class CommonlyTreatedWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                categories = json.loads(value)
            except Exception:
                categories = []
        elif isinstance(value, list):
            categories = value
        else:
            categories = []
            
        categories_json = json.dumps(categories)
        categories_json_escaped = escape(categories_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - CommonlyTreatedWidget */
        #cms-treated-{id_str} {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        }}
        .cms-widget-container {{
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }}
        .cms-card {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #1e293b !important;
        }}
        .cms-card-title {{
            color: #0f172a !important;
        }}
        .cms-input-field {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }}
        .cms-input-field::placeholder {{
            color: #94a3b8 !important;
        }}
        .cms-form-box {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }}
        
        /* Dark Mode overrides */
        html.dark #cms-treated-{id_str} .cms-widget-container,
        body.dark #cms-treated-{id_str} .cms-widget-container,
        .dark #cms-treated-{id_str} .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark #cms-treated-{id_str} .cms-card,
        body.dark #cms-treated-{id_str} .cms-card,
        .dark #cms-treated-{id_str} .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-card-title,
        body.dark #cms-treated-{id_str} .cms-card-title,
        .dark #cms-treated-{id_str} .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark #cms-treated-{id_str} .cms-input-field,
        body.dark #cms-treated-{id_str} .cms-input-field,
        .dark #cms-treated-{id_str} .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark #cms-treated-{id_str} .cms-input-field::placeholder,
        body.dark #cms-treated-{id_str} .cms-input-field::placeholder,
        .dark #cms-treated-{id_str} .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-form-box,
        body.dark #cms-treated-{id_str} .cms-form-box,
        .dark #cms-treated-{id_str} .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-label,
        body.dark #cms-treated-{id_str} .cms-label,
        .dark #cms-treated-{id_str} .cms-label {{
            color: #94a3b8 !important;
        }}
        </style>
        
        <div id="cms-treated-{id_str}" 
             x-data="{{ 
                 categories: {categories_json_escaped},
                 newCatTitle: '',
                 newCatIcon: 'PlusSquare',
                 newCatItemsText: '',
                 
                 addCategory() {{
                     let title = this.newCatTitle.trim();
                     if (!title) {{
                         alert('Category title cannot be empty.');
                         return;
                     }}
                     if (this.categories.some(cat => cat.title.toLowerCase() === title.toLowerCase())) {{
                         alert('A category with this title already exists.');
                         return;
                     }}
                     let itemsList = [];
                     if (this.newCatItemsText.trim()) {{
                         itemsList = this.newCatItemsText.split(/[\\n,]+/).map(item => item.trim()).filter(item => item.length > 0);
                     }}
                     this.categories.push({{
                         title: title,
                         icon: this.newCatIcon,
                         items: itemsList
                     }});
                     this.newCatTitle = '';
                     this.newCatIcon = 'PlusSquare';
                     this.newCatItemsText = '';
                 }},
                 removeCategory(idx) {{
                     if (confirm('Are you sure you want to remove this category?')) {{
                         this.categories.splice(idx, 1);
                     }}
                 }},
                 
                 // Add item dynamically to existing category
                 newItemText: {{}},
                 addItem(catIdx) {{
                     let text = (this.newItemText[catIdx] || '').trim();
                     if (!text) return;
                     if (this.categories[catIdx].items.some(item => item.toLowerCase() === text.toLowerCase())) {{
                         alert('This item already exists in this category.');
                         return;
                     }}
                     this.categories[catIdx].items.push(text);
                     this.newItemText[catIdx] = '';
                 }},
                 removeItem(catIdx, itemIdx) {{
                     this.categories[catIdx].items.splice(itemIdx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(categories)">{categories_json_escaped}</textarea>
            
            <!-- List of Categories -->
            <div class="space-y-4 max-h-[400px] overflow-y-auto pr-1">
                <template x-for="(cat, catIdx) in categories" :key="catIdx">
                    <div class="cms-card p-4 border rounded-xl shadow-sm relative space-y-3 hover:border-slate-350 transition-colors">
                        <!-- Header with Title & Icon & Delete Button -->
                        <div class="flex items-center justify-between border-b border-slate-100 pb-2 gap-3">
                            <div class="flex flex-wrap items-center gap-3 flex-1">
                                <div class="flex items-center gap-1.5">
                                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Title:</span>
                                    <input type="text" x-model="cat.title" placeholder="Category Title"
                                           class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg w-full max-w-[150px] focus:outline-none focus:border-sky-500 transition-colors" />
                                </div>
                                <div class="flex items-center gap-1.5">
                                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Icon:</span>
                                    <select x-model="cat.icon" 
                                            class="cms-input-field text-[11px] px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors">
                                        <option value="PlusSquare">PlusSquare (Upper)</option>
                                        <option value="Triangle">Triangle (Lower)</option>
                                        <option value="Hexagon">Hexagon (Joint/Complex)</option>
                                        <option value="ShieldCheck">ShieldCheck</option>
                                        <option value="Activity">Activity</option>
                                        <option value="Zap">Zap</option>
                                        <option value="HeartPulse">HeartPulse</option>
                                    </select>
                                </div>
                            </div>
                            <button type="button" class="text-red-500 hover:bg-red-50 p-1 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeCategory(catIdx)">
                                <span class="material-symbols-outlined align-middle" style="font-size: 18px;">delete</span>
                            </button>
                        </div>
                        
                        <!-- List of items under this category -->
                        <div class="space-y-1.5 pl-2">
                            <template x-for="(item, itemIdx) in cat.items" :key="itemIdx">
                                <div class="flex items-center justify-between text-xs text-slate-600 dark:text-slate-300 py-1 px-2 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg gap-2">
                                    <div class="flex items-center gap-2 flex-1">
                                        <span class="w-1.5 h-1.5 bg-sky-500 rounded-full flex-shrink-0"></span>
                                        <input type="text" x-model="cat.items[itemIdx]"
                                               class="cms-input-field text-xs bg-transparent border-0 border-b border-slate-100 hover:border-slate-200 focus:border-sky-500 focus:outline-none w-full py-0.5" />
                                    </div>
                                    <button type="button" class="text-red-400 hover:text-red-650 border-0 bg-transparent cursor-pointer p-0.5 flex items-center justify-center flex-shrink-0" @click="removeItem(catIdx, itemIdx)">
                                        <span class="material-symbols-outlined align-middle" style="font-size: 14px;">close</span>
                                    </button>
                                </div>
                            </template>
                            <div x-show="!cat.items || cat.items.length === 0">
                                <p class="text-[10px] text-slate-400 italic">No items in this category.</p>
                            </div>
                        </div>
                        
                        <!-- Add Inline Item Form -->
                        <div class="flex gap-2 pt-2 border-t border-slate-50 mt-2">
                            <input type="text" 
                                   x-model="newItemText[catIdx]" 
                                   @keydown.enter.prevent="addItem(catIdx)" 
                                   placeholder="Add new item to this category..." 
                                   class="cms-input-field flex-1 text-[11px] px-2 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                            <button type="button" 
                                    @click="addItem(catIdx)"
                                    class="px-3 py-1 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[9px] rounded-lg transition-all uppercase tracking-wider border-0 cursor-pointer">
                                Add Item
                            </button>
                        </div>
                    </div>
                </template>
                <div x-show="categories.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No categories added yet.</p>
                </div>
            </div>
            
            <!-- Add New Category Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add New Category</h4>
                <div class="grid sm:grid-cols-2 gap-3">
                    <div class="space-y-1">
                        <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Category Title</label>
                        <input type="text" x-model="newCatTitle" placeholder="Category Title (e.g. Upper Limb)" 
                               class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                    </div>
                    <div class="space-y-1">
                        <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Icon Type</label>
                        <select x-model="newCatIcon" 
                                class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors">
                            <option value="PlusSquare">PlusSquare (Upper Limb)</option>
                            <option value="Triangle">Triangle (Lower Limb)</option>
                            <option value="Hexagon">Hexagon (Joint & Complex Trauma)</option>
                            <option value="ShieldCheck">ShieldCheck</option>
                            <option value="Activity">Activity</option>
                            <option value="Zap">Zap</option>
                            <option value="HeartPulse">HeartPulse</option>
                        </select>
                    </div>
                </div>
                
                <div class="space-y-1">
                    <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Initial Items (comma or newline separated)</label>
                    <textarea x-model="newCatItemsText" rows="2" placeholder="Item 1&#10;Item 2&#10;Item 3" 
                              class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors"></textarea>
                </div>

                <button type="button" @click="addCategory()" 
                        class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add Category
                </button>
            </div>
        </div>
        """
        return mark_safe(html)



class JourneyStepsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f'''
        <style>
        #cms-journey-{id_str} {{ font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
        .cms-widget-container {{ background-color: #f8fafc !important; border-color: #e2e8f0 !important; }}
        .cms-card {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #1e293b !important; }}
        .cms-card-title {{ color: #0f172a !important; }}
        .cms-card-desc {{ color: #475569 !important; }}
        .cms-input-field {{ background-color: #ffffff !important; border-color: #cbd5e1 !important; color: #0f172a !important; }}
        .cms-input-field::placeholder {{ color: #94a3b8 !important; }}
        .cms-form-box {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; }}
        html.dark #cms-journey-{id_str} .cms-widget-container, body.dark #cms-journey-{id_str} .cms-widget-container, .dark #cms-journey-{id_str} .cms-widget-container {{ background-color: #0f172a !important; border-color: #1e293b !important; }}
        html.dark #cms-journey-{id_str} .cms-card, body.dark #cms-journey-{id_str} .cms-card, .dark #cms-journey-{id_str} .cms-card {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-journey-{id_str} .cms-card-title, body.dark #cms-journey-{id_str} .cms-card-title, .dark #cms-journey-{id_str} .cms-card-title {{ color: #f8fafc !important; }}
        html.dark #cms-journey-{id_str} .cms-card-desc, body.dark #cms-journey-{id_str} .cms-card-desc, .dark #cms-journey-{id_str} .cms-card-desc {{ color: #94a3b8 !important; }}
        html.dark #cms-journey-{id_str} .cms-input-field, body.dark #cms-journey-{id_str} .cms-input-field, .dark #cms-journey-{id_str} .cms-input-field {{ background-color: #0f172a !important; border-color: #334155 !important; color: #f8fafc !important; }}
        html.dark #cms-journey-{id_str} .cms-input-field::placeholder, body.dark #cms-journey-{id_str} .cms-input-field::placeholder, .dark #cms-journey-{id_str} .cms-input-field::placeholder {{ color: #475569 !important; }}
        html.dark #cms-journey-{id_str} .cms-form-box, body.dark #cms-journey-{id_str} .cms-form-box, .dark #cms-journey-{id_str} .cms-form-box {{ background-color: #1e293b !important; border-color: #334155 !important; }}
        html.dark #cms-journey-{id_str} .cms-label, body.dark #cms-journey-{id_str} .cms-label, .dark #cms-journey-{id_str} .cms-label {{ color: #94a3b8 !important; }}
        </style>
        
        <div id="cms-journey-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newNum: '',
                 newTitle: '',
                 newDesc: '',
                 addItem() {{
                     if (this.newTitle.trim() && this.newDesc.trim()) {{
                         this.items.push({{
                             number: this.newNum.trim() || String(this.items.length + 1).padStart(2, '0'),
                             title: this.newTitle.trim(),
                             description: this.newDesc.trim()
                         }});
                         this.newNum = '';
                         this.newTitle = '';
                         this.newDesc = '';
                     }} else {{
                         alert('Title and Description are required.');
                     }}
                 }},
                 removeItem(idx) {{
                     if (confirm('Remove this step?')) {{
                         this.items.splice(idx, 1);
                     }}
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <div class="space-y-3 max-h-[400px] overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-4 border rounded-xl shadow-sm relative space-y-2 hover:border-slate-350 transition-colors">
                        <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                            <div class="flex gap-2 items-center w-full">
                                <span class="text-[10px] text-slate-400">Num:</span>
                                <input type="text" x-model="item.number" class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 w-16" />
                                <span class="text-[10px] text-slate-400 ml-2">Title:</span>
                                <input type="text" x-model="item.title" class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 flex-1" />
                            </div>
                            <button type="button" class="text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent cursor-pointer ml-2" @click="removeItem(idx)">
                                <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                            </button>
                        </div>
                        <div class="flex flex-col gap-1">
                            <span class="text-[10px] text-slate-400">Description:</span>
                            <textarea x-model="item.description" class="cms-input-field w-full text-xs px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500" rows="2"></textarea>
                        </div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No journey steps added yet.</p>
                </div>
            </div>
            
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add New Step</h4>
                <div class="grid sm:grid-cols-3 gap-2">
                    <input type="text" x-model="newNum" placeholder="Num (e.g. 01)" class="cms-input-field text-xs px-3 py-2 border rounded-lg" />
                    <input type="text" x-model="newTitle" placeholder="Title" class="cms-input-field text-xs px-3 py-2 border rounded-lg col-span-2" />
                </div>
                <textarea x-model="newDesc" rows="2" placeholder="Description..." class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg"></textarea>
                <button type="button" @click="addItem()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg border-0 cursor-pointer uppercase tracking-wider">
                    Add Step
                </button>
            </div>
        </div>
        '''
        return mark_safe(html)


class FaqWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f'''
        <style>
        #cms-faq-{id_str} {{ font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
        .cms-widget-container {{ background-color: #f8fafc !important; border-color: #e2e8f0 !important; }}
        .cms-card {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #1e293b !important; }}
        .cms-card-title {{ color: #0f172a !important; }}
        .cms-input-field {{ background-color: #ffffff !important; border-color: #cbd5e1 !important; color: #0f172a !important; }}
        .cms-input-field::placeholder {{ color: #94a3b8 !important; }}
        .cms-form-box {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; }}
        .cms-btn-secondary {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #334155 !important; }}
        .cms-btn-secondary:hover {{ background-color: #e2e8f0 !important; color: #0f172a !important; }}
        html.dark #cms-faq-{id_str} .cms-widget-container, body.dark #cms-faq-{id_str} .cms-widget-container, .dark #cms-faq-{id_str} .cms-widget-container {{ background-color: #0f172a !important; border-color: #1e293b !important; }}
        html.dark #cms-faq-{id_str} .cms-card, body.dark #cms-faq-{id_str} .cms-card, .dark #cms-faq-{id_str} .cms-card {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-faq-{id_str} .cms-card-title, body.dark #cms-faq-{id_str} .cms-card-title, .dark #cms-faq-{id_str} .cms-card-title {{ color: #f8fafc !important; }}
        html.dark #cms-faq-{id_str} .cms-input-field, body.dark #cms-faq-{id_str} .cms-input-field, .dark #cms-faq-{id_str} .cms-input-field {{ background-color: #0f172a !important; border-color: #334155 !important; color: #f8fafc !important; }}
        html.dark #cms-faq-{id_str} .cms-input-field::placeholder, body.dark #cms-faq-{id_str} .cms-input-field::placeholder, .dark #cms-faq-{id_str} .cms-input-field::placeholder {{ color: #475569 !important; }}
        html.dark #cms-faq-{id_str} .cms-form-box, body.dark #cms-faq-{id_str} .cms-form-box, .dark #cms-faq-{id_str} .cms-form-box {{ background-color: #1e293b !important; border-color: #334155 !important; }}
        html.dark #cms-faq-{id_str} .cms-btn-secondary, body.dark #cms-faq-{id_str} .cms-btn-secondary, .dark #cms-faq-{id_str} .cms-btn-secondary {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-faq-{id_str} .cms-btn-secondary:hover, body.dark #cms-faq-{id_str} .cms-btn-secondary:hover, .dark #cms-faq-{id_str} .cms-btn-secondary:hover {{ background-color: #334155 !important; color: #f8fafc !important; }}
        </style>
        
        <div id="cms-faq-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 minimized: {{}},
                 allMinimized: false,
                 newQuestion: '',
                 newAnswer: '',
                 isItemMinimized(idx) {{
                     return this.minimized[idx] === true;
                 }},
                 toggleItem(idx) {{
                     this.minimized[idx] = !this.isItemMinimized(idx);
                 }},
                 toggleAll() {{
                     this.allMinimized = !this.allMinimized;
                     this.items.forEach((_, idx) => {{
                         this.minimized[idx] = this.allMinimized;
                     }});
                 }},
                 moveUp(idx) {{
                     if (idx > 0) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx - 1];
                         this.items[idx - 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx - 1];
                         this.minimized[idx - 1] = tempMin;
                     }}
                 }},
                 moveDown(idx) {{
                     if (idx < this.items.length - 1) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx + 1];
                         this.items[idx + 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx + 1];
                         this.minimized[idx + 1] = tempMin;
                     }}
                 }},
                 addItem() {{
                     if (this.newQuestion.trim() && this.newAnswer.trim()) {{
                         this.items.push({{
                             question: this.newQuestion.trim(),
                             answer: this.newAnswer.trim()
                         }});
                         this.minimized[this.items.length - 1] = false;
                         this.newQuestion = '';
                         this.newAnswer = '';
                     }} else {{
                         alert('Question and Answer are required.');
                     }}
                 }},
                 removeItem(idx) {{
                     if (confirm('Remove this FAQ item?')) {{
                         this.items.splice(idx, 1);
                         delete this.minimized[idx];
                     }}
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-3xl mt-1"
        >
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- Header Toolbar -->
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <div class="flex items-center gap-2">
                    <span class="font-bold text-xs text-slate-700 dark:text-slate-200 uppercase tracking-wide">FAQ Items</span>
                    <span class="text-[11px] bg-sky-100 dark:bg-sky-950 text-sky-700 dark:text-sky-300 font-semibold px-2 py-0.5 rounded-full" x-text="items.length + ' FAQs'"></span>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" 
                            @click="toggleAll()" 
                            class="cms-btn-secondary flex items-center gap-1.5 px-3 py-1.5 border rounded-lg text-xs font-semibold cursor-pointer transition-all shadow-sm">
                        <span class="material-symbols-outlined text-sm" x-text="allMinimized ? 'unfold_more' : 'unfold_less'" style="font-size: 16px;"></span>
                        <span x-text="allMinimized ? 'Expand All' : 'Minimize All'"></span>
                    </button>
                </div>
            </div>

            <!-- FAQs List -->
            <div class="space-y-3 max-h-[500px] overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-3.5 border rounded-xl shadow-sm relative space-y-3 hover:border-slate-350 transition-all">
                        <!-- Header Bar -->
                        <div class="flex items-center justify-between gap-3">
                            <div class="flex items-center gap-2 flex-1 min-w-0 cursor-pointer select-none" @click="toggleItem(idx)">
                                <span class="shrink-0 w-6 h-6 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold text-[10px] flex items-center justify-center" x-text="'#' + (idx + 1)"></span>
                                <span class="text-xs font-bold truncate flex-1 text-slate-800 dark:text-slate-100" x-text="item.question || '(Empty question...)'"></span>
                            </div>
                            
                            <div class="flex items-center gap-1 shrink-0">
                                <!-- Move Up/Down -->
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === 0" 
                                        @click="moveUp(idx)"
                                        title="Move Up">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_upward</span>
                                </button>
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === items.length - 1" 
                                        @click="moveDown(idx)"
                                        title="Move Down">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_downward</span>
                                </button>
                                
                                <!-- Minimize / Expand Toggle Button -->
                                <button type="button" 
                                        class="flex items-center gap-1 text-[11px] font-medium px-2 py-1 rounded-md text-sky-600 dark:text-sky-400 hover:bg-sky-50 dark:hover:bg-sky-950 border border-sky-200 dark:border-sky-800 bg-transparent cursor-pointer"
                                        @click="toggleItem(idx)"
                                        :title="isItemMinimized(idx) ? 'Expand' : 'Minimize'">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 15px;" x-text="isItemMinimized(idx) ? 'expand_more' : 'expand_less'"></span>
                                    <span x-text="isItemMinimized(idx) ? 'Expand' : 'Minimize'"></span>
                                </button>

                                <!-- Delete Button -->
                                <button type="button" 
                                        class="text-red-500 hover:bg-red-50 dark:hover:bg-red-950 p-1 rounded-md border-0 bg-transparent cursor-pointer" 
                                        @click="removeItem(idx)"
                                        title="Delete FAQ">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                                </button>
                            </div>
                        </div>

                        <!-- Collapsible Content Body -->
                        <div x-show="!isItemMinimized(idx)" class="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Question:</label>
                                <input type="text" 
                                       x-model="item.question" 
                                       placeholder="Enter question..." 
                                       class="cms-input-field text-xs font-semibold px-3 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full" />
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Answer:</label>
                                <textarea x-model="item.answer" 
                                          placeholder="Enter answer..." 
                                          class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500" 
                                          rows="3"></textarea>
                            </div>
                        </div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-xs text-slate-400 italic py-3 text-center">No FAQs added yet.</p>
                </div>
            </div>
            
            <!-- Add New FAQ Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <div class="flex items-center gap-1.5 border-b border-slate-100 dark:border-slate-800 pb-2">
                    <span class="material-symbols-outlined text-sky-500" style="font-size: 16px;">add_circle</span>
                    <h4 class="text-[11px] font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wide m-0">Add New FAQ</h4>
                </div>
                <input type="text" x-model="newQuestion" placeholder="Question..." class="cms-input-field text-xs px-3 py-2 border rounded-lg w-full" />
                <textarea x-model="newAnswer" rows="2" placeholder="Answer..." class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg"></textarea>
                <button type="button" @click="addItem()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-lg border-0 cursor-pointer uppercase tracking-wider transition-colors shadow-sm">
                    + Add FAQ
                </button>
            </div>
        </div>
        '''
        return mark_safe(html)


class SportsInjuryItemsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f'''
        <style>
        #cms-sports-{id_str} {{ font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
        .cms-widget-container {{ background-color: #f8fafc !important; border-color: #e2e8f0 !important; }}
        .cms-card {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #1e293b !important; }}
        .cms-card-title {{ color: #0f172a !important; }}
        .cms-input-field {{ background-color: #ffffff !important; border-color: #cbd5e1 !important; color: #0f172a !important; }}
        .cms-input-field::placeholder {{ color: #94a3b8 !important; }}
        .cms-form-box {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; }}
        .cms-btn-secondary {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #334155 !important; }}
        .cms-btn-secondary:hover {{ background-color: #e2e8f0 !important; color: #0f172a !important; }}
        html.dark #cms-sports-{id_str} .cms-widget-container, body.dark #cms-sports-{id_str} .cms-widget-container, .dark #cms-sports-{id_str} .cms-widget-container {{ background-color: #0f172a !important; border-color: #1e293b !important; }}
        html.dark #cms-sports-{id_str} .cms-card, body.dark #cms-sports-{id_str} .cms-card, .dark #cms-sports-{id_str} .cms-card {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-sports-{id_str} .cms-card-title, body.dark #cms-sports-{id_str} .cms-card-title, .dark #cms-sports-{id_str} .cms-card-title {{ color: #f8fafc !important; }}
        html.dark #cms-sports-{id_str} .cms-input-field, body.dark #cms-sports-{id_str} .cms-input-field, .dark #cms-sports-{id_str} .cms-input-field {{ background-color: #0f172a !important; border-color: #334155 !important; color: #f8fafc !important; }}
        html.dark #cms-sports-{id_str} .cms-input-field::placeholder, body.dark #cms-sports-{id_str} .cms-input-field::placeholder, .dark #cms-sports-{id_str} .cms-input-field::placeholder {{ color: #475569 !important; }}
        html.dark #cms-sports-{id_str} .cms-form-box, body.dark #cms-sports-{id_str} .cms-form-box, .dark #cms-sports-{id_str} .cms-form-box {{ background-color: #1e293b !important; border-color: #334155 !important; }}
        html.dark #cms-sports-{id_str} .cms-btn-secondary, body.dark #cms-sports-{id_str} .cms-btn-secondary, .dark #cms-sports-{id_str} .cms-btn-secondary {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-sports-{id_str} .cms-btn-secondary:hover, body.dark #cms-sports-{id_str} .cms-btn-secondary:hover, .dark #cms-sports-{id_str} .cms-btn-secondary:hover {{ background-color: #334155 !important; color: #f8fafc !important; }}
        </style>
        
        <div id="cms-sports-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 minimized: {{}},
                 allMinimized: false,
                 newTitle: '',
                 newDesc: '',
                 isItemMinimized(idx) {{
                     return this.minimized[idx] === true;
                 }},
                 toggleItem(idx) {{
                     this.minimized[idx] = !this.isItemMinimized(idx);
                 }},
                 toggleAll() {{
                     this.allMinimized = !this.allMinimized;
                     this.items.forEach((_, idx) => {{
                         this.minimized[idx] = this.allMinimized;
                     }});
                 }},
                 moveUp(idx) {{
                     if (idx > 0) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx - 1];
                         this.items[idx - 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx - 1];
                         this.minimized[idx - 1] = tempMin;
                     }}
                 }},
                 moveDown(idx) {{
                     if (idx < this.items.length - 1) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx + 1];
                         this.items[idx + 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx + 1];
                         this.minimized[idx + 1] = tempMin;
                     }}
                 }},
                 addItem() {{
                     if (this.newTitle.trim() && this.newDesc.trim()) {{
                         this.items.push({{
                             title: this.newTitle.trim(),
                             desc: this.newDesc.trim()
                         }});
                         this.minimized[this.items.length - 1] = false;
                         this.newTitle = '';
                         this.newDesc = '';
                     }} else {{
                         alert('Point Title and Description are required.');
                     }}
                 }},
                 removeItem(idx) {{
                     if (confirm('Remove this feature point?')) {{
                         this.items.splice(idx, 1);
                         delete this.minimized[idx];
                     }}
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-3xl mt-1"
        >
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- Header Toolbar -->
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <div class="flex items-center gap-2">
                    <span class="font-bold text-xs text-slate-700 dark:text-slate-200 uppercase tracking-wide">Treatment & Recovery Points</span>
                    <span class="text-[11px] bg-sky-100 dark:bg-sky-950 text-sky-700 dark:text-sky-300 font-semibold px-2 py-0.5 rounded-full" x-text="items.length + ' Points'"></span>
                </div>
                <div class="flex items-center gap-2">
                    <!-- Minimize / Expand All Button -->
                    <button type="button" 
                            @click="toggleAll()" 
                            class="cms-btn-secondary flex items-center gap-1.5 px-3 py-1.5 border rounded-lg text-xs font-semibold cursor-pointer transition-all shadow-sm">
                        <span class="material-symbols-outlined text-sm" x-text="allMinimized ? 'unfold_more' : 'unfold_less'" style="font-size: 16px;"></span>
                        <span x-text="allMinimized ? 'Expand All' : 'Minimize All'"></span>
                    </button>
                </div>
            </div>

            <!-- Items List -->
            <div class="space-y-3 max-h-[500px] overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-3.5 border rounded-xl shadow-sm relative space-y-3 hover:border-slate-350 transition-all">
                        <!-- Card Header -->
                        <div class="flex items-center justify-between gap-3">
                            <div class="flex items-center gap-2 flex-1 min-w-0 cursor-pointer select-none" @click="toggleItem(idx)">
                                <span class="shrink-0 w-6 h-6 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold text-[10px] flex items-center justify-center" x-text="'#' + (idx + 1)"></span>
                                <span class="text-xs font-bold truncate flex-1 text-slate-800 dark:text-slate-100" x-text="item.title || '(Empty title...)'"></span>
                            </div>
                            
                            <div class="flex items-center gap-1 shrink-0">
                                <!-- Move Up/Down -->
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === 0" 
                                        @click="moveUp(idx)"
                                        title="Move Up">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_upward</span>
                                </button>
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === items.length - 1" 
                                        @click="moveDown(idx)"
                                        title="Move Down">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_downward</span>
                                </button>
                                
                                <!-- Minimize / Expand Single Item Button -->
                                <button type="button" 
                                        class="flex items-center gap-1 text-[11px] font-medium px-2 py-1 rounded-md text-sky-600 dark:text-sky-400 hover:bg-sky-50 dark:hover:bg-sky-950 border border-sky-200 dark:border-sky-800 bg-transparent cursor-pointer"
                                        @click="toggleItem(idx)"
                                        :title="isItemMinimized(idx) ? 'Expand' : 'Minimize'">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 15px;" x-text="isItemMinimized(idx) ? 'expand_more' : 'expand_less'"></span>
                                    <span x-text="isItemMinimized(idx) ? 'Expand' : 'Minimize'"></span>
                                </button>

                                <!-- Delete Button -->
                                <button type="button" 
                                        class="text-red-500 hover:bg-red-50 dark:hover:bg-red-950 p-1 rounded-md border-0 bg-transparent cursor-pointer" 
                                        @click="removeItem(idx)"
                                        title="Delete Item">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                                </button>
                            </div>
                        </div>

                        <!-- Collapsible Content Body -->
                        <div x-show="!isItemMinimized(idx)" class="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Point Title:</label>
                                <input type="text" 
                                       x-model="item.title" 
                                       placeholder="Enter point title..." 
                                       class="cms-input-field text-xs font-semibold px-3 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full" />
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Point Description:</label>
                                <textarea x-model="item.desc" 
                                          placeholder="Enter description..." 
                                          class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500" 
                                          rows="2"></textarea>
                            </div>
                        </div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-xs text-slate-400 italic py-3 text-center">No points added yet.</p>
                </div>
            </div>
            
            <!-- Add New Point Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <div class="flex items-center gap-1.5 border-b border-slate-100 dark:border-slate-800 pb-2">
                    <span class="material-symbols-outlined text-sky-500" style="font-size: 16px;">add_circle</span>
                    <h4 class="text-[11px] font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wide m-0">Add New Treatment Point</h4>
                </div>
                <input type="text" x-model="newTitle" placeholder="Point Title (e.g. Comprehensive Clinical Assessment)" class="cms-input-field text-xs px-3 py-2 border rounded-lg w-full" />
                <textarea x-model="newDesc" rows="2" placeholder="Point Description..." class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg"></textarea>
                <button type="button" @click="addItem()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-lg border-0 cursor-pointer uppercase tracking-wider transition-colors shadow-sm">
                    + Add Treatment Point
                </button>
            </div>
        </div>
        '''
        return mark_safe(html)


class TrustCardsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f'''
        <style>
        #cms-trust-{id_str} {{ font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
        .cms-widget-container {{ background-color: #f8fafc !important; border-color: #e2e8f0 !important; }}
        .cms-card {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #1e293b !important; }}
        .cms-card-title {{ color: #0f172a !important; }}
        .cms-input-field {{ background-color: #ffffff !important; border-color: #cbd5e1 !important; color: #0f172a !important; }}
        .cms-input-field::placeholder {{ color: #94a3b8 !important; }}
        .cms-form-box {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; }}
        .cms-btn-secondary {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; color: #334155 !important; }}
        .cms-btn-secondary:hover {{ background-color: #e2e8f0 !important; color: #0f172a !important; }}
        html.dark #cms-trust-{id_str} .cms-widget-container, body.dark #cms-trust-{id_str} .cms-widget-container, .dark #cms-trust-{id_str} .cms-widget-container {{ background-color: #0f172a !important; border-color: #1e293b !important; }}
        html.dark #cms-trust-{id_str} .cms-card, body.dark #cms-trust-{id_str} .cms-card, .dark #cms-trust-{id_str} .cms-card {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-trust-{id_str} .cms-card-title, body.dark #cms-trust-{id_str} .cms-card-title, .dark #cms-trust-{id_str} .cms-card-title {{ color: #f8fafc !important; }}
        html.dark #cms-trust-{id_str} .cms-input-field, body.dark #cms-trust-{id_str} .cms-input-field, .dark #cms-trust-{id_str} .cms-input-field {{ background-color: #0f172a !important; border-color: #334155 !important; color: #f8fafc !important; }}
        html.dark #cms-trust-{id_str} .cms-input-field::placeholder, body.dark #cms-trust-{id_str} .cms-input-field::placeholder, .dark #cms-trust-{id_str} .cms-input-field::placeholder {{ color: #475569 !important; }}
        html.dark #cms-trust-{id_str} .cms-form-box, body.dark #cms-trust-{id_str} .cms-form-box, .dark #cms-trust-{id_str} .cms-form-box {{ background-color: #1e293b !important; border-color: #334155 !important; }}
        html.dark #cms-trust-{id_str} .cms-btn-secondary, body.dark #cms-trust-{id_str} .cms-btn-secondary, .dark #cms-trust-{id_str} .cms-btn-secondary {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-trust-{id_str} .cms-btn-secondary:hover, body.dark #cms-trust-{id_str} .cms-btn-secondary:hover, .dark #cms-trust-{id_str} .cms-btn-secondary:hover {{ background-color: #334155 !important; color: #f8fafc !important; }}
        </style>
        
        <div id="cms-trust-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 minimized: {{}},
                 allMinimized: false,
                 newId: '',
                 newIcon: 'Award',
                 newTitle: '',
                 newDesc: '',
                 newBadge: '',
                 isItemMinimized(idx) {{
                     return this.minimized[idx] === true;
                 }},
                 toggleItem(idx) {{
                     this.minimized[idx] = !this.isItemMinimized(idx);
                 }},
                 toggleAll() {{
                     this.allMinimized = !this.allMinimized;
                     this.items.forEach((_, idx) => {{
                         this.minimized[idx] = this.allMinimized;
                     }});
                 }},
                 moveUp(idx) {{
                     if (idx > 0) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx - 1];
                         this.items[idx - 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx - 1];
                         this.minimized[idx - 1] = tempMin;
                     }}
                 }},
                 moveDown(idx) {{
                     if (idx < this.items.length - 1) {{
                         const temp = this.items[idx];
                         this.items[idx] = this.items[idx + 1];
                         this.items[idx + 1] = temp;
                         const tempMin = this.minimized[idx];
                         this.minimized[idx] = this.minimized[idx + 1];
                         this.minimized[idx + 1] = tempMin;
                     }}
                 }},
                 addItem() {{
                     const titleVal = (this.newTitle || '').trim();
                     if (!titleVal) {{
                         alert('Please enter a Title for the trust card.');
                         return;
                     }}
                     const idVal = (this.newId || '').trim() || String(this.items.length + 1).padStart(2, '0');
                     const iconVal = this.newIcon || 'Award';
                     const descVal = (this.newDesc || '').trim();
                     const badgeVal = (this.newBadge || '').trim();
                     
                     this.items.push({{
                         id: idVal,
                         icon: iconVal,
                         title: titleVal,
                         description: descVal,
                         badge: badgeVal
                     }});
                     this.minimized[this.items.length - 1] = false;
                     this.newId = '';
                     this.newIcon = 'Award';
                     this.newTitle = '';
                     this.newDesc = '';
                     this.newBadge = '';
                 }},
                 removeItem(idx) {{
                     if (confirm('Remove this trust card?')) {{
                         this.items.splice(idx, 1);
                         delete this.minimized[idx];
                     }}
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-3xl mt-1"
        >
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- Header Toolbar -->
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <div class="flex items-center gap-2">
                    <span class="font-bold text-xs text-slate-700 dark:text-slate-200 uppercase tracking-wide">Trust Feature Cards</span>
                    <span class="text-[11px] bg-sky-100 dark:bg-sky-950 text-sky-700 dark:text-sky-300 font-semibold px-2 py-0.5 rounded-full" x-text="items.length + ' Cards'"></span>
                </div>
                <div class="flex items-center gap-2">
                    <!-- Minimize / Expand All Button -->
                    <button type="button" 
                            @click="toggleAll()" 
                            class="cms-btn-secondary flex items-center gap-1.5 px-3 py-1.5 border rounded-lg text-xs font-semibold cursor-pointer transition-all shadow-sm">
                        <span class="material-symbols-outlined text-sm" x-text="allMinimized ? 'unfold_more' : 'unfold_less'" style="font-size: 16px;"></span>
                        <span x-text="allMinimized ? 'Expand All' : 'Minimize All'"></span>
                    </button>
                </div>
            </div>

            <!-- Items List -->
            <div class="space-y-3 max-h-[500px] overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-3.5 border rounded-xl shadow-sm relative space-y-3 hover:border-slate-350 transition-all">
                        <!-- Card Header -->
                        <div class="flex items-center justify-between gap-3">
                            <div class="flex items-center gap-2 flex-1 min-w-0 cursor-pointer select-none" @click="toggleItem(idx)">
                                <span class="shrink-0 w-8 h-6 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold text-[10px] flex items-center justify-center font-mono" x-text="item.id || '#' + (idx + 1)"></span>
                                <span class="text-xs font-bold truncate flex-1 text-slate-800 dark:text-slate-100" x-text="item.title || '(Empty title...)'"></span>
                                <span class="text-[10px] bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-300 px-2 py-0.5 rounded font-semibold shrink-0" x-text="item.badge || item.icon"></span>
                            </div>
                            
                            <div class="flex items-center gap-1 shrink-0">
                                <!-- Move Up/Down -->
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === 0" 
                                        @click="moveUp(idx)"
                                        title="Move Up">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_upward</span>
                                </button>
                                <button type="button" 
                                        class="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 border-0 bg-transparent cursor-pointer disabled:opacity-30" 
                                        :disabled="idx === items.length - 1" 
                                        @click="moveDown(idx)"
                                        title="Move Down">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">arrow_downward</span>
                                </button>
                                
                                <!-- Minimize / Expand Single Item Button -->
                                <button type="button" 
                                        class="flex items-center gap-1 text-[11px] font-medium px-2 py-1 rounded-md text-sky-600 dark:text-sky-400 hover:bg-sky-50 dark:hover:bg-sky-950 border border-sky-200 dark:border-sky-800 bg-transparent cursor-pointer"
                                        @click="toggleItem(idx)"
                                        :title="isItemMinimized(idx) ? 'Expand' : 'Minimize'">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 15px;" x-text="isItemMinimized(idx) ? 'expand_more' : 'expand_less'"></span>
                                    <span x-text="isItemMinimized(idx) ? 'Expand' : 'Minimize'"></span>
                                </button>

                                <!-- Delete Button -->
                                <button type="button" 
                                        class="text-red-500 hover:bg-red-50 dark:hover:bg-red-950 p-1 rounded-md border-0 bg-transparent cursor-pointer" 
                                        @click="removeItem(idx)"
                                        title="Delete Card">
                                    <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                                </button>
                            </div>
                        </div>

                        <!-- Collapsible Content Body -->
                        <div x-show="!isItemMinimized(idx)" class="space-y-3 pt-2 border-t border-slate-100 dark:border-slate-800">
                            <div class="grid sm:grid-cols-3 gap-2.5">
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Card ID / Number:</label>
                                    <input type="text" 
                                           x-model="item.id" 
                                           placeholder="e.g. 01" 
                                           class="cms-input-field text-xs font-mono font-semibold px-3 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full" />
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Icon:</label>
                                    <select x-model="item.icon" 
                                            class="cms-input-field text-xs px-2.5 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full">
                                        <option value="Award">Award (Experience / Quality)</option>
                                        <option value="Cpu">Cpu (Technology / Robotic)</option>
                                        <option value="Zap">Zap (Fast Recovery / Energy)</option>
                                        <option value="HeartHandshake">HeartHandshake (Personalized Care)</option>
                                        <option value="ShieldCheck">ShieldCheck (Safety / Trust)</option>
                                        <option value="CheckCircle2">CheckCircle2</option>
                                        <option value="Activity">Activity</option>
                                        <option value="HeartPulse">HeartPulse</option>
                                        <option value="Sparkles">Sparkles</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Badge Tag:</label>
                                    <input type="text" 
                                           x-model="item.badge" 
                                           placeholder="e.g. 14+ Yrs Experience" 
                                           class="cms-input-field text-xs font-semibold px-3 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full" />
                                </div>
                            </div>

                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Card Title:</label>
                                <input type="text" 
                                       x-model="item.title" 
                                       placeholder="e.g. Expert Care" 
                                       class="cms-input-field text-xs font-bold px-3 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 w-full" />
                            </div>

                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Card Description:</label>
                                <textarea x-model="item.description" 
                                          placeholder="Enter description..." 
                                          class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500" 
                                          rows="2"></textarea>
                            </div>
                        </div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-xs text-slate-400 italic py-3 text-center">No trust cards added yet.</p>
                </div>
            </div>
            
            <!-- Add New Trust Card Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <div class="flex items-center gap-1.5 border-b border-slate-100 dark:border-slate-800 pb-2">
                    <span class="material-symbols-outlined text-sky-500" style="font-size: 16px;">add_circle</span>
                    <h4 class="text-[11px] font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wide m-0">Add New Trust Card</h4>
                </div>
                
                <div class="grid sm:grid-cols-3 gap-2.5">
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">ID / Number (Optional):</label>
                        <input type="text" x-model="newId" placeholder="e.g. 05" class="cms-input-field text-xs font-mono px-3 py-2 border rounded-lg w-full" />
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Icon:</label>
                        <select x-model="newIcon" class="cms-input-field text-xs px-3 py-2 border rounded-lg w-full">
                            <option value="Award">Award (Experience)</option>
                            <option value="Cpu">Cpu (Technology)</option>
                            <option value="Zap">Zap (Recovery)</option>
                            <option value="HeartHandshake">HeartHandshake (Care)</option>
                            <option value="ShieldCheck">ShieldCheck</option>
                            <option value="CheckCircle2">CheckCircle2</option>
                            <option value="Activity">Activity</option>
                            <option value="HeartPulse">HeartPulse</option>
                            <option value="Sparkles">Sparkles</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Badge Tag (Optional):</label>
                        <input type="text" x-model="newBadge" placeholder="e.g. Tailored Plans" class="cms-input-field text-xs px-3 py-2 border rounded-lg w-full" />
                    </div>
                </div>
                
                <div>
                    <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Card Title <span class="text-red-500">*</span>:</label>
                    <input type="text" 
                           x-model="newTitle" 
                           @keydown.enter.prevent="addItem()" 
                           placeholder="Card Title (e.g. Holistic Patient Recovery)" 
                           class="cms-input-field text-xs px-3 py-2 border rounded-lg w-full" />
                </div>
                
                <div>
                    <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Card Description (Optional):</label>
                    <textarea x-model="newDesc" 
                              @keydown.ctrl.enter.prevent="addItem()" 
                              rows="2" 
                              placeholder="Card Description..." 
                              class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg"></textarea>
                </div>
                
                <button type="button" 
                        @click="addItem()" 
                        class="w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs rounded-lg border-0 cursor-pointer uppercase tracking-wider transition-colors shadow-sm">
                    + Add Trust Card
                </button>
            </div>
        </div>
        '''
        return mark_safe(html)


import re

def clean_schema_markup_data(val):
    """
    Accepts:
    1. Python dict / list
    2. JSON string: '{"@context": "https://schema.org", ...}'
    3. Full HTML script tag string:
       '<script type="application/ld+json">
        {
          "@context": "https://schema.org",
          ...
        }
        </script>'
    
    Returns:
    Parsed Python dict / list (or None if empty)
    """
    if val is None:
        return None
    if isinstance(val, (dict, list)):
        return val
    if isinstance(val, str):
        val = val.strip()
        if not val:
            return None
        
        # Check if wrapped in <script ...> ... </script>
        script_match = re.search(r'<script[^>]*>([\s\S]*?)<\/script>', val, re.IGNORECASE)
        if script_match:
            val = script_match.group(1).strip()
        
        try:
            return json.loads(val)
        except (ValueError, TypeError, json.JSONDecodeError):
            # Attempt to extract outer JSON object or array
            first_brace = val.find('{')
            first_bracket = val.find('[')
            starts = [p for p in [first_brace, first_bracket] if p != -1]
            if starts:
                start = min(starts)
                last_brace = val.rfind('}')
                last_bracket = val.rfind(']')
                ends = [p for p in [last_brace, last_bracket] if p != -1]
                if ends:
                    end = max(ends)
                    if end > start:
                        try:
                            return json.loads(val[start:end+1])
                        except Exception:
                            pass
            return val
    return val


class SchemaMarkupWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        if isinstance(value, (dict, list)):
            display_val = json.dumps(value, indent=2, ensure_ascii=False)
        elif isinstance(value, str):
            display_val = value
        else:
            display_val = ""
            
        escaped_val = escape(display_val)
        
        html = f"""
        <div id="schema-widget-{id_str}" class="cms-widget-container p-4 border rounded-xl my-2" style="background-color: #f8fafc; border-color: #e2e8f0;">
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                        JSON-LD Schema Markup
                    </span>
                    <span class="text-xs text-slate-500">Supports raw JSON or full &lt;script type="application/ld+json"&gt; tags</span>
                </div>
                <button type="button" 
                        onclick="(function(){{
                            const el = document.getElementById('{id_str}');
                            if(!el) return;
                            let v = el.value.trim();
                            const match = v.match(/<script[^>]*>([\\s\\S]*?)<\\/script>/i);
                            if(match) v = match[1].trim();
                            try {{
                                const parsed = JSON.parse(v);
                                el.value = JSON.stringify(parsed, null, 2);
                            }} catch(err) {{
                                alert('JSON formatting error: ' + err.message);
                            }}
                        }})()"
                        class="px-2.5 py-1 text-xs font-semibold text-slate-700 bg-white hover:bg-slate-100 border border-slate-300 rounded shadow-sm cursor-pointer transition-colors">
                    ✨ Format JSON
                </button>
            </div>
            <textarea name="{name}" 
                      id="{id_str}" 
                      rows="14" 
                      class="w-full font-mono text-xs p-3 border rounded-lg focus:ring-2 focus:ring-sky-500 focus:outline-none"
                      style="background-color: #ffffff; color: #0f172a; border-color: #cbd5e1; white-space: pre; tab-size: 2; line-height: 1.5;"
                      placeholder='&lt;script type="application/ld+json"&gt;&#10;{{&#10;  "@context": "https://schema.org",&#10;  "@graph": [&#10;    {{&#10;      "@type": "Physician",&#10;      "name": "Dr. Ulhas Sonar"&#10;    }}&#10;  ]&#10;}}&#10;&lt;/script&gt;'>{escaped_val}</textarea>
            <div class="mt-2 text-[11px] text-slate-500 flex items-center justify-between">
                <span>💡 You can paste either pure JSON or the full <code>&lt;script type="application/ld+json"&gt;...&lt;/script&gt;</code> block here. It will automatically be cleaned and parsed on save.</span>
            </div>
        </div>
        """
        return mark_safe(html)


class SchemaJSONFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', SchemaMarkupWidget())
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value or (isinstance(value, str) and not value.strip()):
            return None
        
        cleaned = clean_schema_markup_data(value)
        if isinstance(cleaned, (dict, list)):
            return cleaned
        if isinstance(cleaned, str):
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f"Invalid JSON in schema markup: {e}")
        return cleaned

    def prepare_value(self, value):
        if value is None:
            return ""
        if isinstance(value, (dict, list)):
            return json.dumps(value, indent=2, ensure_ascii=False)
        return str(value)


class HeroStatsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        initial_items = []
        if isinstance(value, str) and value.strip():
            try:
                initial_items = json.loads(value)
            except (ValueError, TypeError):
                initial_items = []
        elif isinstance(value, list):
            initial_items = value
            
        json_str = json.dumps(initial_items)
        escaped_json = escape(json_str)

        html = f'''
        <div id="hero-stats-widget-{id_str}" class="cms-widget-container p-4 border rounded-xl my-2" 
             x-data="{{
                items: JSON.parse('{escaped_json}' || '[]'),
                newValue: '',
                newSuffix: '+',
                newLabel: '',
                newIsGoogle: false,
                syncHidden() {{
                    const el = document.getElementById('{id_str}');
                    if (el) {{
                        el.value = JSON.stringify(this.items);
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }},
                addItem() {{
                    if (!this.newLabel && !this.newValue) return;
                    this.items.push({{
                        value: this.newValue.trim(),
                        suffix: this.newSuffix.trim(),
                        label: this.newLabel.trim(),
                        isGoogle: !!this.newIsGoogle,
                        isStar: !!this.newIsGoogle
                    }});
                    this.newValue = '';
                    this.newSuffix = '+';
                    this.newLabel = '';
                    this.newIsGoogle = false;
                    this.syncHidden();
                }},
                removeItem(idx) {{
                    this.items.splice(idx, 1);
                    this.syncHidden();
                }},
                moveItem(idx, direction) {{
                    const targetIdx = idx + direction;
                    if (targetIdx < 0 || targetIdx >= this.items.length) return;
                    const temp = this.items[idx];
                    this.items[idx] = this.items[targetIdx];
                    this.items[targetIdx] = temp;
                    this.syncHidden();
                }}
             }}"
             x-init="$watch('items', () => syncHidden())">
             
            <textarea name="{name}" id="{id_str}" style="display:none;" x-text="JSON.stringify(items)">{escaped_json}</textarea>
            
            <div class="flex items-center justify-between border-b pb-3 mb-4">
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-sky-100 text-sky-800 border border-sky-300">
                        Hero Stats Counter Items
                    </span>
                    <span class="text-xs text-slate-500">Live animated numbers displayed in the bottom stats row of the Hero section</span>
                </div>
                <span class="text-xs text-slate-400 font-mono" x-text="items.length + ' item(s)'"></span>
            </div>
            
            <!-- Items List -->
            <div class="space-y-3 mb-5">
                <template x-if="items.length === 0">
                    <div class="text-center py-6 border-2 border-dashed border-slate-200 rounded-xl bg-white text-slate-400 text-xs">
                        No custom hero stats configured yet. Default counters (15+ Exp, 6 Qualifications, 10+ Research, 6+ Audits, 10+ Presentations, 5.0 Google) will be used.
                    </div>
                </template>
                
                <template x-for="(item, index) in items" :key="index">
                    <div class="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-xl shadow-sm hover:border-sky-300 transition-all">
                        <div class="flex flex-col items-center gap-1 shrink-0 text-slate-400">
                            <button type="button" @click="moveItem(index, -1)" class="p-1 hover:text-sky-600 cursor-pointer disabled:opacity-30" :disabled="index === 0">▲</button>
                            <span class="text-[10px] font-mono font-bold text-slate-500" x-text="'#' + (index + 1)"></span>
                            <button type="button" @click="moveItem(index, 1)" class="p-1 hover:text-sky-600 cursor-pointer disabled:opacity-30" :disabled="index === items.length - 1">▼</button>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5 flex-1">
                            <div>
                                <label class="block text-[9px] font-bold uppercase text-slate-400 mb-0.5">Value (Number):</label>
                                <input type="text" x-model="item.value" @input="syncHidden()" class="text-xs font-bold text-slate-800 px-2 py-1.5 border border-slate-300 rounded w-full" placeholder="e.g. 15 or 5.0" />
                            </div>
                            <div>
                                <label class="block text-[9px] font-bold uppercase text-slate-400 mb-0.5">Suffix (e.g. +):</label>
                                <input type="text" x-model="item.suffix" @input="syncHidden()" class="text-xs font-bold text-slate-800 px-2 py-1.5 border border-slate-300 rounded w-full" placeholder="+" />
                            </div>
                            <div class="sm:col-span-2">
                                <label class="block text-[9px] font-bold uppercase text-slate-400 mb-0.5">Label / Subtitle:</label>
                                <input type="text" x-model="item.label" @input="syncHidden()" class="text-xs text-slate-800 px-2 py-1.5 border border-slate-300 rounded w-full" placeholder="Years Clinical Experience" />
                            </div>
                        </div>

                        <div class="flex flex-col items-center justify-center shrink-0 pl-2 border-l border-slate-100">
                            <label class="flex items-center gap-1 text-[10px] font-medium text-slate-600 mb-1 cursor-pointer">
                                <input type="checkbox" x-model="item.isGoogle" @change="item.isStar = item.isGoogle; syncHidden()" class="rounded text-sky-600" />
                                <span>Google ★</span>
                            </label>
                            <button type="button" @click="removeItem(index)" class="px-2 py-1 text-xs text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors" title="Delete">
                                ✕
                            </button>
                        </div>
                    </div>
                </template>
            </div>
            
            <!-- Add New Stat Box -->
            <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
                <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wide">
                    + Add New Hero Stat Counter
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5">
                    <div>
                        <input type="text" x-model="newValue" placeholder="Value (e.g. 20)" class="text-xs px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg w-full" />
                    </div>
                    <div>
                        <input type="text" x-model="newSuffix" placeholder="Suffix (e.g. +)" class="text-xs px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg w-full" />
                    </div>
                    <div>
                        <input type="text" x-model="newLabel" @keydown.enter.prevent="addItem()" placeholder="Label (e.g. Surgeries Done)" class="text-xs px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg w-full" />
                    </div>
                    <div class="flex items-center gap-2">
                        <label class="flex items-center gap-1 text-xs text-slate-600 cursor-pointer">
                            <input type="checkbox" x-model="newIsGoogle" class="rounded text-sky-600" />
                            <span>Star/Rating</span>
                        </label>
                        <button type="button" @click="addItem()" class="flex-1 py-1.5 bg-sky-600 hover:bg-sky-700 text-white font-bold text-xs rounded-lg uppercase tracking-wider transition-colors shadow-sm">
                            Add
                        </button>
                    </div>
                </div>
            </div>
        </div>
        '''
        return mark_safe(html)




