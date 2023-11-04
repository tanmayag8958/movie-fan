<template>
    <div class="card m-0 p-0 filter-header">
        <h2 class="header-name p-3">MOVIE FAN</h2>
    </div>
    <div class="container dashboard-container" style="max-width: 95% !important;">
        <div class="row">
            <div
                    v-for="countTile in countTiles"
                    :key="countTile['tile_key']"
                    :class="'col-' + Math.floor(6/countTiles.length).toString()"
            >
                <tile-viewer
                        :tile="countTile"
                        :selected-filters="selectedFilters"
                        :selected-media="selectedMedia"
                />
            </div>
            <div
                    v-for="_filter in filters"
                    :key="_filter['name']"
                    class="col-2"
            >
                <div class="card card-container">
                    <div class="card-body p-0">
                        <div class="row display-flex justify-content-center align-items-center m-auto">
                            <div class="col-10 p-4 filter-container">
                                <span class="filter-label">{{ _filter['label'] }}: </span>
                                <span class="filter-label"> {{ selectedFilters[_filter['name']] }} </span>
                            </div>
                            <div class="col-2 float-right p-0">
                                <div class="dropdown" style="cursor:pointer;">
                                    <div class="dropdown-toggle filter-dropdown" id="dropdownMenuButton"
                                         data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    </div>
                                    <div class="dropdown-menu dropdown-menu-right dropdown-menu-container"
                                         aria-labelledby="dropdownMenuButton">
                                        <a
                                                v-for="(value, valueIndex) in _filter['values']"
                                                :key="_filter['name'] + '-' + value"
                                                class="dropdown-item"
                                                :class="valueIndex === _filter['values'].length - 1 ? '' : 'dropdown-border-bottom'"
                                                @click="handleFilterSelection(_filter['name'], value)"
                                        >
                                            {{ value }}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-2 display-flex justify-content-center align-items-center">
                <div class="row">
                    <div
                            v-for="(media, mediaIndex) in mediaObjects"
                            :key="media['name']"
                            class="col-6"
                            :style="mediaIndex === mediaObjects.length - 1 ? {'padding-left': '0'} : {'padding-right': '0'}"
                    >
                        <button
                                class="btn dashboard-button p-3"
                                :class="media['selected'] ? 'alert-success' : ''"
                                :style="mediaIndex === mediaObjects.length - 1 ? {'border-left': '0'} : {'border-right': '0'}"
                                @click="handleMediaChange(media['name'])"
                        >
                            {{ media['label'] }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <template v-if="chartTiles.length">
            <div class="row pt-5">
                <div
                        v-for="chartTile in chartTiles"
                        :key="chartTile['tile_key']"
                        class="col-6"
                >
                    <tile-viewer
                            :tile="chartTile"
                            :selected-filters="selectedFilters"
                            :selected-media="selectedMedia"
                    />
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import axios from "axios";
import TileViewer from "@/components/Tile.vue";

export default {
    name: 'DashboardViewer',
    components: {
        TileViewer
    },
    data() {
        return {
            filters: [],
            selectedFilters: {},
            tiles: [],
            chartTiles: [],
            countTiles: [],
            mediaObjects: [
                {
                    'name': 'movie',
                    'label': 'Movie',
                    'selected': false
                },
                {
                    'name': 'series',
                    'label': 'Series',
                    'selected': true
                }
            ]
        }
    },
    computed: {
        selectedMedia() {
            let selectedMedia;
            this.mediaObjects.forEach(media => {
                if (media['selected']) selectedMedia = media;
            });
            return selectedMedia;
        }
    },
    mounted: function () {
        this.setup();
        this.fetchFilters();
        this.fetchTiles();
    },
    methods: {
        deepCopy: function (value) {
            return JSON.parse(JSON.stringify(value))
        },
        saveToLocalStorage: function (container) {
            let savedData = JSON.parse(localStorage.savedData || null) || {};
            savedData = {...savedData, ...container};
            localStorage.savedData = JSON.stringify(savedData);
        },
        getFromLocalStorage: function (key) {
            let savedData = JSON.parse(localStorage.savedData || null) || {};
            return savedData[key] || null;
        },
        setup: function () {
            const selectedMediaName = this.getFromLocalStorage('selectedMediaName');
            if (selectedMediaName) this.handleMediaChange(selectedMediaName);
        },
        handleMediaChange: function (mediaName) {
            if (mediaName === this.selectedMedia['name']) return;
            this.mediaObjects.forEach(media => {
                media['selected'] = media['name'] === mediaName;
            });
            this.saveToLocalStorage({'selectedMediaName': mediaName});
            this.$nextTick(() => {
                this.emitter.emit('media-changes');
            });
        },
        handleFilterSelection: function (filterName, valueSelected) {
            let currentFilters = this.deepCopy(this.selectedFilters);
            currentFilters[filterName] = valueSelected;
            this.selectedFilters = Object.assign({}, currentFilters);
        },
        fetchTiles: function () {
            axios({
                method: 'get',
                url: 'http://localhost:8000/dashboard/tiles/' + `?media=${this.selectedMedia['name']}`,
            }).then(response => {
                this.tiles = response.data;
                this.tiles.forEach(tile => {
                    if (tile['type'] === 'chart') {
                        this.chartTiles.push(tile);
                    } else if (tile['type'] === 'count') {
                        this.countTiles.push(tile);
                    }
                });
            });
        },

        fetchFilters: function () {
            axios({
                method: 'get',
                url: 'http://localhost:8000/data/filters/',
            }).then(response => {
                const response_data = response.data;
                response_data.forEach(_filter => {
                    this.selectedFilters[_filter['name']] = 'Select';
                });
                this.filters = response_data;
                this.filters.forEach(_filter => {
                    _filter['values'] = ['Select'].concat(_filter['values'])
                });
            });
        }
    }
}
</script>
<style>
.dashboard-container {
    margin-top: 4%;
}

.card-container {
    background-color: #2B2B2B;
    border: none;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
}

.filter-header {
    background-color: #2B2B2B;
    border: none;
}

.header-name {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-label {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-dropdown {
    color: white;
    font-size: 20px;
}

.filter-container {
    border-right: 1px solid #3e3e3e;
    padding-left: 3px !important;
    padding-right: 3px !important;
}

.dropdown-menu-container {
    overflow-y: auto;
    position: absolute !important;
    height: 500px;
    scroll-behavior: smooth;
    background-color: #2B2B2B;
    border: none;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;
}

.dashboard-button {
    border-radius: 0;
    border: 8px solid #2B2B2B;
    font-weight: 800;
    width: 100%;
    box-sizing: border-box;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
}

.dropdown-border-bottom {
    border-bottom: 1px solid #353535;
}
</style>