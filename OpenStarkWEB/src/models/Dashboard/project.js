import { message } from 'antd';
import {
  queryProjectNotice,
  queryProjectsList,
  editProjects,
  deleteProjects,
  getTeams,
  queryJacocoList,
  JacocoChart,
} from '@/services/admin';

export default {
  namespace: 'project',

  state: {
    notice: [],
    projects: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    teams: [],
    projectsList: [],
    editResult: undefined,
    jacocoData: [],
    jacocoList: [],
    chartJacoco: undefined,
  },

  effects: {
    *fetchNotice(_, { call, put }) {
      const response = yield call(queryProjectNotice);
      yield put({
        type: 'saveNotice',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *fetchProjects({ payload }, { call, put }) {
      const response = yield call(queryProjectsList, payload);
      yield put({
        type: 'saveProjects',
        payload: response && response.data,
      });
    },
    *fetchJacoco({ payload, callback }, { call, put }) {
      const response = yield call(queryJacocoList, payload);
      if(response && response.status === 'FAIL'){
        message.error(response.message);
        yield put({
          type: 'saveJacoco',
          payload: [],
        });
        yield put({
          type: 'chartJacoco',
          payload: undefined,
        });
      }else{
        // eslint-disable-next-line no-unused-expressions
        !!callback && callback(response && typeof(response.data) === 'object' ? response.data : []);
      }
    },
    *JacocoChart({ payload }, { call, put }) {
      const response = yield call(JacocoChart, payload);
      yield put({
        type: 'chartJacoco',
        payload: response && typeof(response.data) === 'object' ? response.data : {},
      });
    },
    *editProjects({ payload, callback }, { call, put }) {
      const response = yield call(editProjects, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *deleteProjects({ payload, callback }, { call, put }) {
      const response = yield call(deleteProjects, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *fetchTeams({ payload }, { call, put }) {
      const response = yield call(getTeams, payload);
      yield put({
        type: 'saveTeamsData',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
  },

  reducers: {
    saveNotice(state, { payload }) {
      return {
        ...state,
        notice: payload,
      };
    },
    saveProjects(state, { payload }) {
      if (payload && payload.type === 'projects') {
        return {
          ...state,
          projectsList: payload && Array.isArray(payload.data) ? payload.data : [],
        };
      }
      return {
        ...state,
        projects: payload && typeof payload === 'object' ? payload : {},
      };
    },
    saveJacoco(state, { payload }) {
      return {
        ...state,
        jacocoData: payload || [],
      };
    },
    searchJacoco(state, { payload }) {
      return {
        ...state,
        jacocoList: payload && payload.length > 0 ? payload : [{key: 0, title: '无更多结果'}],
      };
    },
    chartJacoco(state, { payload }) {
      return {
        ...state,
        chartJacoco: payload,
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
    saveTeamsData(state, { payload }) {
      return {
        ...state,
        teams: payload,
      };
    },
  },
};
