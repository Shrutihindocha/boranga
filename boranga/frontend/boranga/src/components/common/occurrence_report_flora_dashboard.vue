<template id="species_flora_or_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group" id="select_occurrence">
                        <label for="or_occurrence_lookup">Occurrence:</label>
                            <select 
                                id="or_occurrence_lookup"  
                                name="or_occurrence_lookup"  
                                ref="or_occurrence_lookup" 
                                class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_scientific_name_by_groupname">
                        <label for="or_scientific_name_lookup_by_groupname">Scientific Name:</label>
                            <select 
                                id="or_scientific_name_lookup_by_groupname"  
                                name="or_scientific_name_lookup_by_groupname"  
                                ref="or_scientific_name_lookup_by_groupname" 
                                class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_status">
                        <label for="">Status:</label>
                            <select class="form-select" v-model="filterORFloraStatus">
                                <option value="all">All</option>
                                <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                            </select>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label for="">Submitted From Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="submitted_from_date" v-model="filterORFloraSubmittedFromDate">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label for="">Submitted To Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="submitted_from_date" v-model="filterORFloraSubmittedToDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        <div v-if="addFloraORVisibility && is_for_agenda==false" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFloraOccurrenceReport"><i class="fa-solid fa-circle-plus"></i> Add Occurrence Report</button>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="flora_or_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                />
            </div>
        </div>
    </div>
</template>
<script>
//require('@popperjs/core');
//import { createPopper } from '@popperjs/core';
//require('popperjs');
//require('bootstrap');
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
// var select2 = require('select2');
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'OccurrenceReportFloraTable',
    props: {
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
        group_type_name:{
            type: String,
            required: true
        },
        group_type_id:{
            type: Number,
            required: true,
            default:0
        },
        url:{
            type: String,
            required: true
        },
        // when the datable need to be shown for agenda_items in meeting check this variable is true
        is_for_agenda:{
            type: Boolean,
            default:false
        },
        // for adding agendaitems for the meeting_obj.id
        meeting_obj:{
            type: Object,
            required:false
        },
        filterORFloraOccurrence_cache: {
            type: String,
            required: false,
            default: 'filterORFloraOccurrence',
        },
        filterORFloraScientificName_cache: {
            type: String,
            required: false,
            default: 'filterORFloraScientificName',
        },
        filterORFloraStatus_cache: {
            type: String,
            required: false,
            default: 'filterORFloraStatus',
        },
        filterORFloraSubmittedFromDate_cache: {
            type: String,
            required: false,
            default: 'filterORFloraSubmittedFromDate',
        },
        filterORFloraSubmittedToDate_cache: {
            type: String,
            required: false,
            default: 'filterORFloraSubmittedToDate',
        },

    },
    data() {
        let vm = this;
        return {
            datatable_id: 'species_flora_or-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterORFloraOccurrence: sessionStorage.getItem(this.filterORFloraOccurrence_cache) ? 
                                    sessionStorage.getItem(this.filterORFloraOccurrence_cache) : 'all',
            
            filterORFloraScientificName: sessionStorage.getItem(this.filterORFloraScientificName_cache) ? 
                                sessionStorage.getItem(this.filterORFloraScientificName_cache) : 'all',
            
            filterORFloraStatus: sessionStorage.getItem(this.filterORFloraStatus_cache) ? 
                        sessionStorage.getItem(this.filterORFloraStatus_cache) : 'all',

            filterORFloraSubmittedFromDate: sessionStorage.getItem(this.filterORFloraSubmittedFromDate_cache) ? 
                                sessionStorage.getItem(this.filterORFloraSubmittedFromDate_cache) : '',

            filterORFloraSubmittedToDate: sessionStorage.getItem(this.filterORFloraSubmittedToDate_cache) ? 
                                sessionStorage.getItem(this.filterORFloraSubmittedToDate_cache) : '',

            filterListsSpecies: {},
            occurrence_list: [],
            scientific_name_list: [],
            status_list: [],
            submissions_from_list: [],
            submissions_to_list: [],
            
            // filtering options
            // external_status refers to CUSTOMER_STATUS_CHOICES
            // internal_status referes to PROCESSING_STATUS_CHOICES
            external_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'Under Review'},
                {value: 'with_approver', name: 'Under Review'},
                {value: 'amendment_required', name: 'Amendment Required'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'closed', name: 'DeListed'},
                {value: 'partially_approved', name: 'Partially Approved'},
                {value: 'partially_declined', name: 'Partially Declined'},

            ],
            internal_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'With Assessor'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_approver', name: 'With Approver'},
                {value: 'awaiting_applicant_respone', name: 'Awaiting Applicant Response'},
                {value: 'awaiting_assessor_response', name: 'Awaiting Assessor Response'},
                {value: 'awaiting_responses', name: 'Awaiting Responses'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'closed', name: 'DeListed'},
                {value: 'partially_approved', name: 'Partially Approved'},
                {value: 'partially_declined', name: 'Partially Declined'},
            ],
            
            proposal_status: [],
        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch:{
        filterORFloraOccurrence: function(){
            let vm = this;
            vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterORFloraOccurrence_cache, vm.filterORFloraOccurrence);  
        },
        filterORFloraScientificName: function() {
            let vm = this;
            vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterORFloraScientificName_cache, vm.filterORFloraScientificName);  
        },
        filterORFloraStatus: function() {
            let vm = this;
            vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call. 
            sessionStorage.setItem(vm.filterORFloraStatus_cache, vm.filterORFloraStatus);
        },
        filterORFloraSubmittedFromDate: function() {
            let vm = this;
            vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterORFloraSubmittedFromDate_cache, vm.filterORFloraSubmittedFromDate);  
        },
        filterORFloraSubmittedToDate: function() {
            let vm = this;
            vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterORFloraSubmittedToDate_cache, vm.filterORFloraSubmittedToDate);  
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function(){
            if(this.filterORFloraOccurrence === 'all' && 
                this.filterORFloraScientificName === 'all' && 
                this.filterORFloraStatus === 'all' &&  
                this.filterORFloraSubmittedFromDate === '' && 
                this.filterORFloraSubmittedToDate === ''){
                return false
            } else {
                return true
            }
        },
        is_external: function(){
            return this.level == 'external';
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        addFloraORVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            // Cols for external users be modified
            // if (this.is_external){
            //     return ['Number','Occurrence','Species Scientific Name', 'Submission date/time', 'Submitter', 'Status', 'Action']
            // }
            if (this.is_internal){
                return ['Number','Occurrence','Scientific Name', 'Submission date/time', 'Submitter', 'Status', 'Action']
            }
        },
        column_number: function(){
            return {
                data: "occurrence_report_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.occurrence_report_number
                },
                name: "id",
            }
        },
        column_occurrence: function(){
            return {
                data: "species",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.species){
                        return full.species;
                    }
                    return ''
                },
                name: "species",
            }
        },
        column_scientific_name: function(){
            return {
                data: "scientific_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.scientific_name){
                        return full.scientific_name;
                    }
                    return ''
                },
                name: "scientific_name",
            }
        },
        column_submission_date_time: function(){
            return {
                data: "reported_date",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.reported_date){
                        return full.reported_date;
                    }
                    return ''
                },
                name: "reported_date",
            }
        },
        column_submitter: function(){
            return {
                data: "submitter",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.submitter){
                        return full.submitter;
                    }
                    return ''
                },
                name: "submitter",
            }
        },
        column_status: function(){
            return {
                data: "processing_status_display",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.processing_status_display){
                        return full.processing_status_display;
                    }
                    return ''
                },
                name: "processing_status_display",
            }
        },
        column_action: function(){
            let vm = this
            return {
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if(vm.is_for_agenda==false){
                        if (!vm.is_external){
                            if(full.internal_user_edit)
                            {
                                links +=  `<a href='/internal/conservation_status/${full.id}'>Continue</a><br/>`;
                                links +=  `<a href='#${full.id}' data-discard-cs-proposal='${full.id}'>Discard</a><br/>`;
                            }
                            else{
                                if(full.assessor_process){
                                        links +=  `<a href='/internal/conservation_status/${full.id}'>Process</a><br/>`;
                                }
                                else{
                                    if(full.assessor_edit){
                                        links +=  `<a href='/internal/conservation_status/${full.id}?action=edit'>Edit</a><br/>`;
                                    }
                                    links +=  `<a href='/internal/conservation_status/${full.id}?action=view'>View</a><br/>`;
                                }
                            }
                        }
                    }
                    else{
                        if(vm.meeting_obj.agenda_items_arr.includes(full.id)){
                            links +=  `<a>Added</a><br/>`;
                        }
                        else{
                            links +=  `<a href='#${full.id}' data-add-to-agenda='${full.id}'>Add</a><br/>`;
                        }
                    }
                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = [
                {
                    text: '<i class="fa-solid fa-download"></i> Excel',
                    className: 'btn btn-primary me-2 rounded',
                    action: function (e, dt, node, config) {
                        vm.exportData("excel");
                    }
                },
                {
                    text: '<i class="fa-solid fa-download"></i> CSV',
                    className: 'btn btn-primary rounded',
                    action: function (e, dt, node, config) {
                        vm.exportData("csv");
                    }
                }
            ]
            // if(vm.is_external){
            //     columns = [
            //         vm.column_number,
            //         vm.column_occurrence,
            //         vm.column_scientific_name,
            //         vm.column_submission_date_time, 
            //         vm.column_submitter,
            //         vm.column_status,
            //         vm.column_action,
            //     ]
            //     search = false
            // }
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_occurrence,
                    vm.column_scientific_name,
                    vm.column_submission_date_time, 
                    vm.column_submitter,
                    vm.column_status,
                    vm.column_action,
                ]
                search = true
            }

            return {
                autoWidth: false,
                language: {
                    processing: "<b>Loading...</b>"
                },
                order: [
                    [0, 'desc']
                ],
                lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                responsive: true,
                serverSide: true,
                searching: search,
                 //  to show the "workflow Status","Action" columns always in the last position
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 3, targets: -1 },
                    { responsivePriority: 2, targets: -2 }
                ],
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.filter_group_type = vm.group_type_name;
                        d.filter_occurrence = vm.filterORFloraOccurrence;
                        d.filter_scientific_name = vm.filterORFloraScientificName;
                        d.filter_status = vm.filterORFloraStatus;
                        d.filter_submitted_from_date = vm.filterORFloraSubmittedFromDate;
                        d.filter_submitted_to_date = vm.filterORFloraSubmittedToDate;
                        d.is_internal = vm.is_internal;
                    }
                },
                //dom: 'lBfrtip',
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: vm.is_for_agenda==false?buttons:[],

                columns: columns,
                processing: true,
                initComplete: function() {
                    helpers.enablePopovers();
                },
            }
        }
    
    },
    methods:{
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseOccurrenceLookup: function(){
                let vm = this;
                $(vm.$refs.or_occurrence_lookup).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#select_occurrence"),
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Occurrence",
                    ajax: {
                        url: api_endpoints.species_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterORFloraOccurrence = data;
                    sessionStorage.setItem("filterORFloraOccurrenceText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterORFloraOccurrence = 'all';
                    sessionStorage.setItem("filterORFloraOccurrenceText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-or_occurrence_lookup-results"]')
                    searchField[0].focus();
                });
        },
        initialiseScientificNameLookup: function(){
                let vm = this;
                $(vm.$refs.or_scientific_name_lookup_by_groupname).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#select_scientific_name_by_groupname"),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder:"Select Scientific Name",
                    ajax: {
                        url: api_endpoints.scientific_name_lookup_by_groupname,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterORFloraScientificName = data;
                    sessionStorage.setItem("filterORFloraScientificNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterORFloraScientificName = 'all';
                    sessionStorage.setItem("filterORFloraScientificNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-or_scientific_name_lookup_by_groupname-results"]')
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function(){
            let vm = this;
            //large FilterList of Species Values object
            vm.$http.get(api_endpoints.filter_lists_species+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsSpecies = response.body;
                vm.occurrence_list = vm.filterListsSpecies.occurrence_list;
                vm.scientific_name_list = vm.filterListsSpecies.scientific_name_list;
                vm.status_list = vm.filterListsSpecies.status_list;
                vm.submissions_from_list = vm.filterListsSpecies.submissions_from_list;
                vm.submissions_to_list = vm.filterListsSpecies.submissions_to_list;
                // vm.filterConservationCategory();
                // vm.filterDistrict();
                vm.proposal_status = vm.internal_status.slice().sort((a, b) => {
                        return a.name.trim().localeCompare(b.name.trim());
                    });
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            },(error) => {
                console.log(error);
            })
        },
        createFloraOccurrenceReport: async function () {
            let newFloraCSId = null
            try {
                    const createUrl = api_endpoints.conservation_status+"/";
                    let payload = new Object();
                    payload.application_type_id = this.group_type_id
                    payload.internal_application = true
                    let savedFloraCS = await Vue.http.post(createUrl, payload);
                    if (savedFloraCS) {
                        newFloraCSId = savedFloraCS.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-conservation_status',
                params: {conservation_status_id: newFloraCSId},
                });
        },
        discardCSProposal:function (conservation_status_id) {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then((swalresult) => {
                if(swalresult.isConfirmed){
                    vm.$http.delete(api_endpoints.discard_cs_proposal(conservation_status_id))
                    .then((response) => {
                        swal.fire({
                            title: 'Discarded',
                            text: 'Your proposal has been discarded',
                            icon: 'success',
                            confirmButtonColor:'#226fbb',
                        });
                        vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
                    }, (error) => {
                        console.log(error);
                    });
                }
            },(error) => {

            });
        },
        addToMeetingAgenda:function (conservation_status_id) {
            let vm=this;
            let payload = new Object();
            payload.conservation_status_id = conservation_status_id;
            Vue.http.post(`/api/meeting/${vm.meeting_obj.id}/add_agenda_item.json`,payload).then(res => {
                vm.meeting_obj.agenda_items_arr=res.body;
                vm.$refs.flora_or_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
                this.$emit('updateAgendaItems');
            },
            err => {
              console.log(err);
            });
        },
        addEventListeners: function(){
            let vm = this;
            // internal Discard listener
            vm.$refs.flora_or_datatable.vmDataTable.on('click', 'a[data-discard-cs-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-cs-proposal');
                vm.discardCSProposal(id);
            });

            vm.$refs.flora_or_datatable.vmDataTable.on('click', 'a[data-add-to-agenda]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-add-to-agenda');
                vm.addToMeetingAgenda(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.flora_or_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        fetchProfile: function(){
            let vm = this;
            /*Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body;
                vm.is_payment_admin=response.body.is_payment_admin;
                              
            },(error) => {
                console.log(error);
                
            })*/
        },

        check_assessor: function(proposal){
            let vm = this;
            if (proposal.assigned_officer)
                {
                    { if(proposal.assigned_officer== vm.profile.full_name)
                        return true;
                    else
                        return false;
                }
            }
            else{
                 var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id=vm.profile.id)
                });
                
                if (assessor.length > 0)
                    return true;
                else
                    return false;
              
            }
            
        },
        exportData: function (format) {
            let vm = this;
            const columns_new = {
                "0": {
                    "data": "occurrence",
                    "name": "conservation_status__id, conservation_status__occurrence_report_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "1": {
                    "data": "species_number",
                    "name": "conservation_status__species__species_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "2": {
                    "data": "scientific_name",
                    "name": "occurrence_report__species__taxonomy__scientific_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "3": {
                    "data": "conservation_list",
                    "name": "conservation_status__conservation_list__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "4": {
                    "data": "conservation_category",
                    "name": "conservation_status__conservation_category__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
            };

            const object_load = {
                columns: columns_new,
                filter_group_type: vm.group_type_name,
                filter_occurrence: vm.filterORFloraOccurrence,
                filter_scientific_name: vm.filterORFloraScientificName,
                filter_status: vm.filterORFloraStatus,
                filter_submitted_from_date: vm.filterORFloraSubmittedFromDate,
                filter_submitted_to_date: vm.filterORFloraSubmittedToDate,
                is_internal: vm.is_internal,
                export_format: format
            };

            const url = api_endpoints.species_cs_internal_export;
            const keyValuePairs = [];

            for (const key in object_load) {
                if (object_load.hasOwnProperty(key)) {
                    const encodedKey = encodeURIComponent(key);
                    let encodedValue = '';

                    if (typeof object_load[key] === 'object') {
                        encodedValue = encodeURIComponent(JSON.stringify(object_load[key]));
                    }
                    else {
                        encodedValue = encodeURIComponent(object_load[key]);
                    }
                    keyValuePairs.push(`${encodedKey}=${encodedValue}`);
                }
            }
            const params = keyValuePairs.join('&');
            const fullUrl = `${url}?${params}`;
            try {
                if (format === "excel") {
                    $.ajax({
                        type: "GET",
                        url: fullUrl,
                        contentType: "application/vnd.ms-excel",
                        dataType: "binary",
                        xhrFields: {
                            responseType: 'blob'
                        },

                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "application/vnd.ms-excel" });

                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
                else if (format === "csv") {
                    $.ajax({
                        type: "GET",
                        url: fullUrl,
                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "text/csv" });

                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
            }
            catch (err) {
                console.log(err);
                if (vm.is_internal) {
                    return err;
                }
            }
        },
    },


    mounted: function(){
        this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseOccurrenceLookup();
            vm.initialiseScientificNameLookup();
            //vm.initialiseSearch();
            vm.addEventListeners();
            
            // -- to set the select2 field with the session value if exists onload()
            if(sessionStorage.getItem("filterORFloraOccurrence")!='all' && sessionStorage.getItem("filterORFloraOccurrence")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterORFloraOccurrenceText"), vm.filterORFloraOccurrence, false, true);
                $('#or_occurrence_lookup').append(newOption);
                //$('#scientific_name_lookup').append(newOption).trigger('change');
            }
            if(sessionStorage.getItem("filterORFloraScientificName")!='all' && sessionStorage.getItem("filterORFloraScientificName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterORFloraScientificNameText"), vm.filterORFloraScientificName, false, true);
                $('#or_scientific_name_lookup_by_groupname').append(newOption);
            }
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
.collapse-icon {
    cursor: pointer;
}
.collapse-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '-';
    color: white;
    background-color: #d33333;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}
.expand-icon {
    cursor: pointer;
}
.expand-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '+';
    color: white;
    background-color: #337ab7;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}

</style>
