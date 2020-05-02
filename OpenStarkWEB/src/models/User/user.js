import { message } from 'antd';
import { query as queryUsers, queryCurrent, editCurrent, sendActiveMail } from '@/services/user';
import { getLink, addLink, getOwnLink, deleteLink, getDepartments } from '@/services/admin';

export default {
  namespace: 'user',

  state: {
    list: [],
    currentUser: {},
    navLinks: [],
    navOwnLinks: [],
    editResult: undefined,
    departments: [],
  },

  effects: {
    *getDepartments(_, { call, put }) {
      const response = yield call(getDepartments);
      yield put({
        type: 'departments',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *fetch(_, { call, put }) {
      const response = yield call(queryUsers);
      yield put({
        type: 'save',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *fetchCurrent(_, { call, put }) {
      const response = yield call(queryCurrent);
      yield put({
        type: 'saveCurrentUser',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *editCurrent({ payload }, { call, put }) {
      const response = yield call(editCurrent, payload);
      yield put({
        type: 'editStatus',
        payload: response,
      });
    },
    *getLink(_, { call, put }) {
      const response = yield call(getLink);
      yield put({
        type: 'fetchLink',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *getOwnLink(_, { call, put }) {
      const response = yield call(getOwnLink);
      yield put({
        type: 'fetchOwnLink',
        payload: response && Array.isArray(response.data) ? response.data : [],
      });
    },
    *addLink({ payload, callback }, { call, put }) {
      const response = yield call(addLink, payload);
      yield put({
        type: 'saveLink',
        payload: response,
      });
      if(callback){callback()};
    },
    *deleteLink({ payload, callback }, { call, put }) {
      const response = yield call(deleteLink, payload);
      yield put({
        type: 'deleteOwnLink',
        payload: response,
      });
      if(callback){callback()};
    },
    *sendActiveMail({callback}, { call, put }) {
      const response = yield call(sendActiveMail);
      yield put({
        type: 'editStatus',
        payload: response,
      });
      if(callback){callback()};
    },
  },

  reducers: {
    departments(state, { payload }) {
      return {
        ...state,
        departments: payload,
      };
    },
    save(state, { payload }) {
      return {
        ...state,
        list: payload,
      };
    },
    fetchLink(state, { payload }) {
      return {
        ...state,
        navLinks: payload,
      };
    },
    fetchOwnLink(state, { payload }) {
      return {
        ...state,
        navOwnLinks: payload,
      };
    },
    saveLink(state, { payload }) {
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
    deleteOwnLink(state, { payload }) {
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
    saveCurrentUser(state, { payload }) {
      return {
        ...state,
        currentUser: payload,
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
    changeNotifyCount(state, { payload }) {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          notifyCount: payload.totalCount,
          unreadCount: payload.unreadCount,
        },
      };
    },
  },
};
