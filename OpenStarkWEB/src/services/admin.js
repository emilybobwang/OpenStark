import { isArray } from 'util';
import { stringify } from 'qs';
import request from '../utils/request';

export async function fetchConfig() {
  return request('/api/py/config/system');
}

export async function editConfig(params) {
  return request('/api/py/config/system', {
    method: 'POST',
    body: params,
  });
}

export async function queryProjectNotice() {
  return request('/api/py/project/notice');
}

export async function queryProjectsList(params) {
  return request(`/api/py/project/getProjects?${stringify(params)}`);
}

export async function queryJacocoList(params) {
  return request(`/api/py/jacoco/reports?${stringify(params)}`);
}

export async function JacocoChart(params) {
  return request('/api/py/jacoco/reports', {
    method: 'POST',
    body: params,
  });
}

export async function editProjects(params) {
  return request('/api/py/project/editProjects/edit', {
    method: 'POST',
    body: params,
  });
}

export async function deleteProjects(params) {
  return request('/api/py/project/editProjects/delete', {
    method: 'POST',
    body: params,
  });
}

export async function queryActivities() {
  return request('/api/py/user/activities');
}

export async function editGroup(params) {
  return request('/api/py/group/editTeams/edit', {
    method: 'POST',
    body: params,
  });
}

export async function deleteGroup(params) {
  return request('/api/py/group/editTeams/delete', {
    method: 'POST',
    body: params,
  });
}

export async function getTeams(params) {
  return request(`/api/py/group/getTeams?${stringify(params)}`);
}

export async function fetchChartData(params) {
  let urlParams = '';
  if (isArray(params)) {
    params.forEach(param => {
      urlParams += stringify(param);
      urlParams += '&';
    });
  } else {
    urlParams = stringify(params);
  }
  return request(`/api/py/chart/toolStatistics?${urlParams.slice(0, -1)}`);
}

export async function fetchLoadData(params) {
  return request(`/api/py/chart/performance?${stringify(params)}`);
}

export async function fetchLoadAPI(type, params) {
  return request(`/api/py/chart/performance/${type}?${stringify(params)}`);
}

export async function editLoadAPI(type, params) {
  return request(`/api/py/chart/performance/${type}`, {
    method: 'POST',
    body: params,
  });
}

export async function queryTags() {
  return request('/api/py/tags');
}

export async function queryNotices() {
  return request('/api/py/user/notices');
}

export async function getDepartments() {
  return request('/api/py/getDepartments');
}

export async function getCommonInfo() {
  return request('/api/py/getCommonInfo');
}

export async function clearNotices(params) {
  return request('/api/py/user/notices', {
    method: 'POST',
    body: params,
  });
}

export async function getLink() {
  return request('/api/py/user/navLink/all');
}

export async function addLink(params) {
  return request('/api/py/user/navLink/edit', {
    method: 'POST',
    body: params,
  });
}

export async function getOwnLink() {
  return request('/api/py/user/navLink/own');
}

export async function deleteLink(params) {
  return request('/api/py/user/navLink/delete', {
    method: 'POST',
    body: params,
  });
}

export async function getEnv(op, action, params) {
  return request(`/api/py/env/${op}/${action}?${stringify(params)}`);
}

export async function getConfig(params) {
  return request(`/api/py/synConfig/query?${stringify(params)}`);
}

export async function Reconfig(params) {
  return request('/api/py/synConfig/recovery', {
    method: 'POST',
    body: params,
  });
}

export async function editEnv(op, action, params) {
  return request(`/api/py/env/${op}/${action}`, {
    method: 'POST',
    body: params,
  });
}

export async function getShell(params) {
  return request(`/api/py/tools/shell/list?${stringify(params)}`);
}

export async function runShell(params) {
  return request(`/api/py/tools/shell/run`, {
    method: 'POST',
    body: params,
  });
}

export async function getSQL(params) {
  return request(`/api/py/tools/sql/list?${stringify(params)}`);
}

export async function runSQL(params) {
  return request(`/api/py/tools/sql/run`, {
    method: 'POST',
    body: params,
  });
}

export async function queryToolsList(params) {
  return request(`/api/py/tools/getTools/list?${stringify(params)}`);
}

export async function queryToolsMenu() {
  return request('/api/py/tools/getTools/menu');
}

export async function editTools(params) {
  return request('/api/py/tools/editTools/edit', {
    method: 'POST',
    body: params,
  });
}

export async function deleteTools(params) {
  return request('/api/py/tools/editTools/delete', {
    method: 'POST',
    body: params,
  });
}

export async function synConfig(params) {
  return request(`/api/py/synConfig`, {
    method: 'POST',
    body: params,
  });
}

export async function getKnowledge(op, action, params) {
  return request(`/api/py/knowledge/${op}/${action}?${stringify(params)}`);
}

export async function editKnowledge(op, action, params) {
  return request(`/api/py/knowledge/${op}/${action}`, {
    method: 'POST',
    body: params,
  });
}

export async function getMedias() {
  return request('/api/py/upload/media/files');
}

export async function rmMedias(params) {
  return request('/api/py/upload/media/delete', {
    method: 'POST',
    body: params,
  });
}

export async function fetchTestData(op, action, params) {
  return request(`/api/py/chart/autoTest/${op}/${action}?${stringify(params)}`);
}

export async function getDBs(op, params) {
  return request(`/api/py/syncdb/${op}?${stringify(params)}`);
}

export async function syncDBs(op, params) {
  return request(`/api/py/syncdb/${op}`, {
    method: 'POST',
    body: params,
  });
}

export async function getVers(op, params) {
  return request(`/api/py/tools/diff/${op}?${stringify(params)}`);
}

export async function diffPackages(op, params) {
  return request(`/api/py/tools/diff/${op}`, {
    method: 'POST',
    body: params,
  });
}

export async function getJenkins(op, params) {
  return request(`/api/py/jenkins/${op}?${Array.isArray(params) ? params.map(ele => stringify(ele)).join('&') : stringify(params)}`);
}

export async function runJenkins(op, params) {
  return request(`/api/py/jenkins/${op}`, {
    method: 'POST',
    body: params,
  });
}
