package mobile_web;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.applications.httptools.configurator.HttpController;
import inet.node.inet.StandardHost;

import inet.node.ethernet.Eth10G;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;

import simu5g.nodes.Upf;
import simu5g.nodes.NR.gNodeB;
import simu5g.nodes.NR.NRUe;
import simu5g.nodes.backgroundCell.BackgroundCell;
import simu5g.world.radio.LteChannelControl;
import simu5g.common.binder.Binder;
import simu5g.common.carrierAggregation.CarrierAggregation;
import inet.networklayer.ipv4.RoutingTableRecorder;


network MobileHttpNetwork
{
    submodules:
        httpController: HttpController {
            @display("p=60,201");
        }

        channelControl: LteChannelControl {
            @display("p=50,25;is=s");
        }

        routingRecorder: RoutingTableRecorder {
            @display("p=50,75;is=s");
        }

        server: StandardHost;
        configurator: Ipv4NetworkConfigurator {
            @display("p=69,331");
        }

        binder: Binder;
        carrierAggregation: CarrierAggregation;
        bgCell: BackgroundCell {

            @display("p=326,179");
        }
        ue: NRUe {
            @display("p=326,273");
        }
        router: Router {
            @display("p=69,30");
        }
        upf: Upf {
            @display("p=209,102");
        }
        gnb: gNodeB {

            @display("p=378,126;is=vl");
        }
    connections:
        server.pppg++ <--> Eth10G <--> router.pppg++;
        router.pppg++ <--> Eth10G <--> upf.filterGate;
        upf.pppg++ <--> Eth10G <--> gnb.ppp;



}
