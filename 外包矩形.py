# coding=utf-8
"""
用途：创建一个共面的包裹曲线的矩形框
时间：2023年08月09日
"""

import rhinoscriptsyntax as rs

crv = curve
xl = x_derection_line


def xyplane_curve_boundary_rectangle(icrv):
    """这个曲线处于XY平面时，创造一个共面的包裹曲线的矩形框。"""

    ipts = rs.BoundingBox(icrv)  # 所输曲线的外包矩形框的八个控制点
    iptxs = [ipts[i][0] for i in range(len(ipts))]  # 曲线控制点的所有X数值列表
    iptys = [ipts[i][1] for i in range(len(ipts))]  # 曲线控制点的所有Y数值列表
    """获取曲线的坐标信息"""
    print(iptxs)

    iplane = rs.MovePlane(rs.WorldXYPlane(), rs.AddPoint(min(iptxs), min(iptys), 0))  # 外包矩形所在的平面及原点信息
    irecX = max(iptxs) - min(iptxs)  # 外包矩形的长度
    irecY = max(iptys) - min(iptys)  # 外包矩形的宽度
    ibdrec = rs.AddRectangle(iplane, irecX, irecY)  # 所输曲线的外包矩形
    """通过原点，长，宽建立矩形"""

    return ibdrec


def curve_boundary_rectangle(icrv, ixl):
    """通过旋转使曲线处于XY平面，创造矩形框后旋转回原来平面。"""

    crvnormal = rs.CurveNormal(icrv)    #所输曲线的法线方向
    irefer_o_pt = rs.CurveStartPoint(ixl)   #原有平面的原点
    irefer_x_pt = rs.CurveEndPoint(ixl)     #原有平面的X方向点
    irefer_z_pt = rs.CopyObject(irefer_o_pt, crvnormal)     #原有平面的法线方向点
    ireferpts = [irefer_o_pt, irefer_x_pt, irefer_z_pt]     #原有平面的原点、X方向点和法线方向点的点列表
    itargetpts = [rs.CreatePoint(0, 0, 0), rs.CreatePoint(1, 0, 0), rs.CreatePoint(0, 0, 1)]    #XY平面的原点、X方向点和法线方向点的点列表
    """确定原有平面与XY平面的原点、X方向点和法线方向点"""

    iortcrv = rs.OrientObject(icrv, ireferpts, itargetpts, 1)   #将所输曲线转向XY平面
    ibdrec = xyplane_curve_boundary_rectangle(iortcrv)          #在XY平面上建立外包矩形
    ibdrec = rs.OrientObject(ibdrec, itargetpts, ireferpts, 1)  #将外包矩形转回原来平面
    """通过面与面的转化将矩形框转回原来平面"""

    return ibdrec


if rs.IsCurvePlanar(crv):       #判断所输曲线是否为平面曲线
    bdrec= curve_boundary_rectangle(crv, xl)
else:
    print('curve不是一个平面曲线')
