import { message } from 'antd';
import { editGroup, getTeams, deleteGroup } from '@/services/admin';

export default {
  namespace: 'teams',

  state: {
    groups: [],
    members: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
    editResult: undefined,
  },

  effects: {
    *fetchTeams({ payload }, { call, put }) {
      const response = yield call(getTeams, payload);
      yield put({
        type: 'saveGroupsData',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editTeams({ payload, callback }, { call, put }) {
      const response = yield call(editGroup, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
    *deleteTeams({ payload, callback }, { call, put }) {
      const response = yield call(deleteGroup, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
  },

  reducers: {
    saveGroupsData(state, { payload }) {
      if (payload && payload.groups.length > 0 && payload.members.data.length > 0) {
        return {
          ...state,
          groups: payload.groups,
          members: payload.members,
        };
      }
      if (payload && payload.groups.length > 0) {
        return {
          ...state,
          groups: payload.groups,
        };
      }
      return {
        ...state,
        members: payload.members || {},
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
