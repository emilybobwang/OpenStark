import React, { PureComponent, Fragment } from 'react';
import { Card, Input, AutoComplete, Button, Icon, Divider, Tree } from 'antd';
import { Pie } from '@/components/Charts';
import { connect } from 'dva';
import { goBack } from 'umi/router';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import { AsyncLoadBizCharts } from '@/components/Charts/AsyncLoadBizCharts';

const {Option} = AutoComplete;
const { TreeNode } = Tree;

@connect(({ project, loading }) => ({
  jacocoData: project.jacocoData,
  jacocoList: project.jacocoList,
  chartJacoco: project.chartJacoco,
  loading: loading.effects['project/fetchJacoco'],
  loadingChart: loading.effects['project/JacocoChart'],
}))
class JacocoReportsDetails extends PureComponent {
  componentDidMount(){
    const {
      dispatch,
      match:{params}
    } = this.props;
    dispatch({
      type: 'project/fetchJacoco',
      payload: {
        jid: params.jid,
        date: params.date,
        type: 'package',
      },
      callback: (res) => {
        if(res){
          dispatch({
            type: 'project/saveJacoco',
            payload: res.data,
          });
        }
        dispatch({
          type: 'project/chartJacoco',
          payload: undefined,
        });
      },
    });
  }

  onCheck = (keys, e) => {
    const {dispatch, match:{params}} = this.props;
    dispatch({
      type: 'project/JacocoChart',
      payload: {
        jid: params.jid,
        date: params.date,
        checkedKeys: keys,
        halfCheckedKeys: e.halfCheckedKeys,
      },
    });
  }

  onLoadData = treeNode => new Promise((resolve) => {
    const {props: {dataRef}} = treeNode;
    if (treeNode.props.children || dataRef.key.split('-')[0] === 'method') {
      resolve();
      return;
    }
    const {
      dispatch,
      match:{params}
    } = this.props;
    dispatch({
      type: 'project/fetchJacoco',
      payload: {
        jid: params.jid,
        date: params.date,
        type: dataRef.key.split('-')[0] === 'package' ? 'class' : 'method',
        name: dataRef.key.split('-')[0] === 'package' ? dataRef.package : dataRef.classes,
      },
      callback: (res) => {
        if(res){
          if(res.data.length > 0){
            dataRef.children = res.data;
          }else{
            dataRef.isLeaf = true;
          }
        }
        resolve();
      },
    });
  })

  renderTreeNodes = data => data.map(item => {
    if (item.children) {
      return (
        <TreeNode title={item.title} key={item.key} dataRef={item}>
          {this.renderTreeNodes(item.children)}
        </TreeNode>
      );
    }
    return <TreeNode {...item} dataRef={item} />;
  })

  onSelect = (kw) => {
    if(kw.trim() === '无更多结果'){
      return;
    }
    const {
      dispatch,
      match:{params}
    } = this.props;
    dispatch({
      type: 'project/fetchJacoco',
      payload: {
        jid: params.jid,
        date: params.date,
        name: kw,
        kw,
      },
      callback: (res) => {
        if(res){
          dispatch({
            type: 'project/saveJacoco',
            payload: res.data,
          });
        }
      },
    });
  }

  handleSearch = kw => {
    const { 
      dispatch,
      match:{params}
    } = this.props;
    if(kw.trim() === ''){
      dispatch({
        type: 'project/fetchJacoco',
        payload: {
          jid: params.jid,
          date: params.date,
          type: 'package',
        },
        callback: (res) => {
          if(res){
            dispatch({
              type: 'project/saveJacoco',
              payload: res.data,
            });
          }
        },
      });
      return;
    }
    dispatch({
      type: 'project/fetchJacoco',
      payload: {
        jid: params.jid,
        date: params.date,
        kw: kw.trim(),
      },
      callback: (res) => {
        if(res){
          dispatch({
            type: 'project/searchJacoco',
            payload: res.data,
          });
        }
      },
    });
  }

  onDoubleClick = (_, treeNode) => {
    const {props: {dataRef}} = treeNode;
    const {match:{params}} = this.props;
    if(dataRef.key.split('-')[0] === 'package'){
      window.open(`/static/files/jacoco/${params.jid}/${params.date}/xnol-app/${dataRef.package}/index.html`);
    }else if(dataRef.key.split('-')[0] === 'class'){
      window.open(`/static/files/jacoco/${params.jid}/${params.date}/xnol-app/${dataRef.package}/${dataRef.classes}.html`);
    }else{
      window.open(`/static/files/jacoco/${params.jid}/${params.date}/xnol-app/${dataRef.package}/${dataRef.classes}.java.html`);
    }
  }

  renderOption = item => {
    return (
      <Option key={item.key} value={item.title}>
        {item.title}
      </Option>
    );
  }

  render() {
    const {match:{params}, jacocoData, loading, jacocoList, chartJacoco} = this.props;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card 
            bordered={false} 
            title={(
              <Fragment>
                <Button type="primary" onClick={goBack}>
                  <Icon type="rollback" />
                  返回
                </Button>
                <Divider type="vertical" />
                <a
                  rel="noopener noreferrer"
                  target="_blank"
                  href={`/static/files/jacoco/${params.jid}/${params.date}/index.html`}
                >
                  查看完整版报告
                </a>
              </Fragment>
            )}
            extra={(
              <AutoComplete
                style={{ width: 600 }}
                dataSource={jacocoList.map(this.renderOption)}
                onSelect={this.onSelect}
                onSearch={this.handleSearch}
                placeholder="按包名/类名/方法名搜索"
                allowClear
              >
                <Input
                  suffix={<Icon type="search" style={{color: '#1890FF'}} />}
                />
              </AutoComplete>
            )} 
            loading={jacocoData.length === 0 && loading}
          >
            <Card.Grid style={{height: 800, overflowY: 'auto'}}>
              <Tree loadData={this.onLoadData} loadedKeys={[]} showLine checkable onCheck={this.onCheck} onDoubleClick={this.onDoubleClick}>
                {this.renderTreeNodes(jacocoData)}
              </Tree>
            </Card.Grid>
            <Card.Grid style={{height: 400}}>
              <Pie
                subTitle="行覆盖(LINE)"
                data={chartJacoco && chartJacoco.line}
                total={() => {
                  if (chartJacoco && chartJacoco.line){
                    const total = chartJacoco.line.reduce((pre, now) => now.y + pre, 0);
                    return (
                      <span
                        // eslint-disable-next-line react/no-danger
                        dangerouslySetInnerHTML={{
                          __html: (
                              (chartJacoco.line.reduce(
                                (pre, now) => now.x === 'covered' && now.y + pre,
                                0
                              ) /
                              total) *
                              100
                            )
                              .toFixed(2)
                              .concat('%').concat(' (').concat(total).concat(')'),
                        }}
                      />
                    );
                  }
                  return '';
                }}
              />
            </Card.Grid>
            <Card.Grid style={{height: 400}}>
              <Pie
                subTitle="分支覆盖(BRANCH)"
                data={chartJacoco && chartJacoco.branch}
                total={() => {
                  if (chartJacoco && chartJacoco.branch){
                    const total = chartJacoco.branch.reduce((pre, now) => now.y + pre, 0);
                    return (
                      <span
                        // eslint-disable-next-line react/no-danger
                        dangerouslySetInnerHTML={{
                          __html: (
                              (chartJacoco.branch.reduce(
                                (pre, now) => now.x === 'covered' && now.y + pre,
                                0
                              ) /
                              total) *
                              100
                            )
                              .toFixed(2)
                              .concat('%').concat(' (').concat(total).concat(')'),
                        }}
                      />
                    );
                  }
                  return '';
                }}
              />
            </Card.Grid>
            <Card.Grid style={{height: 400}}>
              <Pie
                subTitle="方法覆盖(METHOD)"
                data={chartJacoco && chartJacoco.method}
                total={() => {
                  if (chartJacoco && chartJacoco.method){
                    const total = chartJacoco.method.reduce((pre, now) => now.y + pre, 0);
                    return (
                      <span
                        // eslint-disable-next-line react/no-danger
                        dangerouslySetInnerHTML={{
                          __html: (
                              (chartJacoco.method.reduce(
                                (pre, now) => now.x === 'covered' && now.y + pre,
                                0
                              ) /
                              total) *
                              100
                            )
                              .toFixed(2)
                              .concat('%').concat(' (').concat(total).concat(')'),
                        }}
                      />
                    );
                  }
                  return '';
                }}
              />
            </Card.Grid>
            <Card.Grid style={{height: 400}}>
              <Pie
                subTitle="类覆盖(CLASS)"
                data={chartJacoco && chartJacoco.classes}
                total={() => {
                  if (chartJacoco && chartJacoco.classes){
                    const total = chartJacoco.classes.reduce((pre, now) => now.y + pre, 0);
                    return (
                      <span
                        // eslint-disable-next-line react/no-danger
                        dangerouslySetInnerHTML={{
                          __html: (
                              (chartJacoco.classes.reduce(
                                (pre, now) => now.x === 'covered' && now.y + pre,
                                0
                              ) /
                              total) *
                              100
                            )
                              .toFixed(2)
                              .concat('%').concat(' (').concat(total).concat(')'),
                        }}
                      />
                    );
                  }
                  return '';
                }}
              />
            </Card.Grid>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default props => (
  <AsyncLoadBizCharts>
    <JacocoReportsDetails {...props} />
  </AsyncLoadBizCharts>
);