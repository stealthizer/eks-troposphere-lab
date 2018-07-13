from troposphere import Template, Parameter, Ref, GetAtt, Output, Export, Sub, Tags
from troposphere.ec2 import VPC, Subnet, InternetGateway, VPCGatewayAttachment, RouteTable, SubnetRouteTableAssociation, Route, EIP, NatGateway


class Vpc(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptre_user_data = sceptre_user_data
        self.add_vpc()
        self.add_public_subnet_a()
        self.add_public_subnet_b()
        self.add_public_subnet_c()
        self.add_internet_gateway()
        self.add_net_gw_vpc_attachment()
        self.add_public_route_table()
        self.add_public_route_association_subnet_a()
        self.add_public_route_association_subnet_b()
        self.add_public_route_association_subnet_c()
        self.add_default_public_route()
        self.add_vpc_output()
        self.add_public_subnet_a_output()
        self.add_public_subnet_b_output()
        self.add_public_subnet_c_output()
        self.add_internet_gateway_output()

    def add_vpc(self):
        self.vpc = self.template.add_resource(VPC(
            "EKSVPC",
            CidrBlock=self.sceptre_user_data["cidr_block"],
            EnableDnsHostnames="true",
            Tags=Tags(
                Name=self.sceptre_user_data["vpc_name"]
            )
        ))

    def add_public_subnet_a(self):
        self.public_subnet_a = self.template.add_resource(Subnet(
            'PublicSubnetA',
            CidrBlock=self.sceptre_user_data["public_subnet_a"],
            MapPublicIpOnLaunch=True,
            VpcId=Ref(self.vpc),
        ))

    def add_public_subnet_b(self):
        self.public_subnet_b = self.template.add_resource(Subnet(
            'PublicSubnetB',
            CidrBlock=self.sceptre_user_data["public_subnet_b"],
            MapPublicIpOnLaunch=True,
            VpcId=Ref(self.vpc),
        ))

    def add_public_subnet_c(self):
        self.public_subnet_c = self.template.add_resource(Subnet(
            'PublicSubnetC',
            CidrBlock=self.sceptre_user_data["public_subnet_c"],
            MapPublicIpOnLaunch=True,
            VpcId=Ref(self.vpc),
        ))

    def add_internet_gateway(self):
        self.internet_gateway = self.template.add_resource(InternetGateway(
            'InternetGateway',
        ))

    def add_net_gw_vpc_attachment(self):
        self.net_gw_vpc_attachment = self.template.add_resource(VPCGatewayAttachment(
            "NatAttachment",
            VpcId=Ref(self.vpc),
            InternetGatewayId=Ref(self.internet_gateway),
        ))

    def add_public_route_table(self):
        self.public_route_table = self.template.add_resource(RouteTable(
            'PublicRouteTable',
            VpcId=Ref(self.vpc),
        ))

    def add_public_route_association_subnet_a(self):
        self.public_route_association_a = self.template.add_resource(SubnetRouteTableAssociation(
            'PublicRouteAssociationA',
            SubnetId=Ref(self.public_subnet_a),
            RouteTableId=Ref(self.public_route_table),
        ))

    def add_public_route_association_subnet_b(self):
        self.public_route_association_b = self.template.add_resource(SubnetRouteTableAssociation(
            'PublicRouteAssociationB',
            SubnetId=Ref(self.public_subnet_b),
            RouteTableId=Ref(self.public_route_table),
        ))

    def add_public_route_association_subnet_c(self):
        self.public_route_association_c = self.template.add_resource(SubnetRouteTableAssociation(
            'PublicRouteAssociationC',
            SubnetId=Ref(self.public_subnet_c),
            RouteTableId=Ref(self.public_route_table),
        ))

    def add_default_public_route(self):
        self.default_public_route = self.template.add_resource(Route(
            'PublicDefaultRoute',
            RouteTableId=Ref(self.public_route_table),
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=Ref(self.internet_gateway),
        ))

    def add_public_subnet_a_output(self):
        self.public_net_output = self.template.add_output(Output(
            "PublicSubnetA",
            Export=Export(Sub("${AWS::StackName}-PublicSubnetA")),
            Description="Public subnet network range",
            Value=Ref("PublicSubnetA"),
        ))

    def add_public_subnet_b_output(self):
        self.public_net_output = self.template.add_output(Output(
            "PublicSubnetB",
            Export=Export(Sub("${AWS::StackName}-PublicSubnetB")),
            Description="Public subnet network range",
            Value=Ref("PublicSubnetB"),
        ))

    def add_public_subnet_c_output(self):
        self.public_net_output = self.template.add_output(Output(
            "PublicSubnetC",
            Export=Export(Sub("${AWS::StackName}-PublicSubnetC")),
            Description="Public subnet network range",
            Value=Ref("PublicSubnetC"),
    ))


    def add_internet_gateway_output(self):
        self.igw_output = self.template.add_output(Output(
            "InternetGateway",
            Description="Internet Gateway",
            Value=Ref(self.internet_gateway),
        ))

    def add_vpc_output(self):
        self.vpc_output = self.template.add_output(Output(
            "VPCId",
            Export=Export(Sub("${AWS::StackName}-VPCId")),
            Description="VPCId of vpc",
            Value=Ref(self.vpc),
        ))


def sceptre_handler(sceptre_user_data):
    vpc = Vpc(sceptre_user_data)
    return vpc.template.to_json()
