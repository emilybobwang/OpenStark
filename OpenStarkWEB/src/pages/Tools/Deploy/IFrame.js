import React, { Component } from 'react';
import { connect } from 'dva';

@connect(({ tools }) => ({
  toolsMenu: tools.toolsMenu,
}))
class IFrame extends Component {
  constructor(props) {
    super(props);
    this.state = {
      iFrameHeight: 600,
      src: props.src,
    };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/fetchToolsMenu',
    });
    this.setState({ iFrameHeight: window.document.body.scrollHeight });
  }

  componentWillReceiveProps(nextProps) {
    if ('toolsMenu' in nextProps) {
      const {
        match: { params },
      } = nextProps;
      nextProps.toolsMenu.forEach(item => {
        if (item.id === params.id || params.id === '0') {
          this.setState({ src: item.url });
        }
      });
    }
  }

  render() {
    const { iFrameHeight, src } = this.state;
    return (
      <iframe
        id="deploy"
        title="deploy"
        src={src}
        width="100%"
        height={iFrameHeight}
        frameBorder="0"
        scrolling="auto"
      />
    );
  }
}

export default IFrame;
