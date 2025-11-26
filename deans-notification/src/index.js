import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import store from "@redux/store";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import * as ROUTES from "src/routes";
import PageHome from "@containers/PageHome";
import PageReport from "@containers/PageReport";
import PageLogin from "@containers/PageLogin";
import PageStaff from "@containers/PageStaff";
import ModalContainer from "@containers/ModalContainer";
import RealTimeConditionTracker from "@containers/RealTimeConditionTracker";
import RealTimeCrisisTracker from "@containers/RealTimeCrisisTracker";

import "src/styles/app.scss";
import "antd/dist/antd.less";

const App = () => (
  <Provider store={store}>
    <React.Fragment>
      <ModalContainer />
      <RealTimeConditionTracker>
        <RealTimeCrisisTracker>
          <Router>
            <Switch>
              <Route exact path={ROUTES.ROUTE_HOME} component={PageHome} />
              <Route path={ROUTES.ROUTE_REPORT} component={PageReport} />
              <Route path={ROUTES.ROUTE_LOGIN} component={PageLogin} />
              <Route path={ROUTES.ROUTE_STAFF} component={PageStaff} />
              {/* fall back main page */}
              <Route path={"/"} component={PageHome} />
            </Switch>
          </Router>
        </RealTimeCrisisTracker>
      </RealTimeConditionTracker>
    </React.Fragment>
  </Provider>
);

ReactDOM.render(<App />, document.getElementById("app"));
