import {
  queryToolsList,
  queryToolsMenu,
  editTools,
  deleteTools,
  getShell,
  runShell,
  getSQL,
  runSQL,
  synConfig,
  getConfig,
  Reconfig,
  getDBs,
  syncDBs,
  getVers,
  diffPackages,
} from '@/services/admin';
import { message } from 'antd';

export default {
  namespace: 'tools',

  state: {
    shellList: [],
    shell: {},
    sqlList: [],
    sql: {},
    tools: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    toolsMenu: [],
    configList: [],
    dbList: [],
    tableList: [],
    initTable: [],
    runResult: undefined,
    editResult: undefined,
  },

  effects: {
    *fetchDBs({ op, payload }, { call, put }) {
      const response = yield call(getDBs, op, payload);
      yield put({
        type: 'saveDBs',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchTools({ payload }, { call, put }) {
      const response = yield call(queryToolsList, payload);
      yield put({
        type: 'saveTools',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *fetchToolsMenu(_, { call, put }) {
      const response = yield call(queryToolsMenu);
      yield put({
        type: 'saveMenu',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *fetchConfig({ payload }, { call, put }) {
      const response = yield call(getConfig, payload);
      yield put({
        type: 'saveConfig',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *editTools({ payload, callback }, { call, put }) {
      const response = yield call(editTools, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *deleteTools({ payload, callback }, { call, put }) {
      const response = yield call(deleteTools, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *getShell({ payload }, { call, put }) {
      const response = yield call(getShell, payload);
      yield put({
        type: 'save',
        payload: response,
      });
    },
    *runShell({ payload }, { call, put }) {
      const response = yield call(runShell, payload);
      yield put({
        type: 'show',
        payload: response,
      });
    },
    *getSQL({ payload }, { call, put }) {
      const response = yield call(getSQL, payload);
      yield put({
        type: 'saveSQL',
        payload: response,
      });
    },
    *runSQL({ payload }, { call, put }) {
      const response = yield call(runSQL, payload);
      yield put({
        type: 'show',
        payload: response,
      });
    },
    *synConfig({ payload }, { call, put }) {
      const response = yield call(synConfig, payload);
      yield put({
        type: 'show',
        payload: response,
      });
    },
    *Reconfig({ payload }, { call, put }) {
      const response = yield call(Reconfig, payload);
      yield put({
        type: 'show',
        payload: response,
      });
    },
    *syncDBs({ op, payload, callback }, { call, put }) {
      const response = yield call(syncDBs, op, payload);
      yield put({
        type: 'show',
        payload: response,
      });
      if(callback){callback()};
    },
    *getVers({ op, payload, callback }, { call, put }) {
      const response = yield call(getVers, op, payload);
      if (op === 'content'){
        // eslint-disable-next-line no-unused-expressions
        !!callback && callback(response);
      }else{
        yield put({
          type: 'saveDBs',
          payload: response && Array.isArray(response.data) ? {tableList: response.data} : {tableList: []},
        });
      }
    },
    *diffPackages({ op, payload }, { call, put }) {
      const response = yield call(diffPackages, op, payload);
      yield put({
        type: 'show',
        payload: response,
      });
    },
  },

  reducers: {
    saveDBs(state, { payload }) {
      return {
        ...state,
        ...payload,
      };
    },
    saveTools(state, { payload }) {
      return {
        ...state,
        tools: payload,
      };
    },
    saveMenu(state, { payload }) {
      return {
        ...state,
        toolsMenu: payload,
      };
    },
    saveConfig(state, { payload }) {
      return {
        ...state,
        configlList: payload,
      };
    },
    save(state, { payload }) {
      if (payload && Array.isArray(payload.data)) {
        return {
          ...state,
          shellList: payload.data,
        };
      }
      return {
        ...state,
        shell: payload && payload.data,
      };
    },
    saveSQL(state, { payload }) {
      if (payload && Array.isArray(payload.data)) {
        return {
          ...state,
          sqlList: payload.data,
        };
      }
      return {
        ...state,
        sql: payload && payload.data,
      };
    },
    show(state, { payload }) {
      return {
        ...state,
        runResult: payload,
      };
    },
    editStatus(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        message.success(payload.message);
      } else {
        message.error(payload && payload.message);
      }
      return {
        ...state,
        editResult: payload,
      };
    },
  },
};
