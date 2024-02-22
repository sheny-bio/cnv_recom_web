#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/25 13:36
# @Author  : shenny
# @File    : views.py
# @Software: PyCharm

from glob import glob
import json
import os.path
import subprocess
from uuid import uuid1
from datetime import datetime

from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.conf import settings

import pandas as pd


def response_json(code=0, msg=None, data=None, status=200, default=None, response=None):
    response = {"code": code, "msg": msg, "data": data} if not response else response
    if default:
        return HttpResponse(json.dumps(response, ensure_ascii=False, default=str), 'application/json', status=status)
    else:
        return HttpResponse(json.dumps(response), 'application/json', status=status)


def home(request):

    job_id = f"{datetime.strftime(datetime.now(), '%Y-%m-%d')}_{uuid1()}"

    if request.GET.get("lang") == "cn":
        return render(request, "page_cnv_recom.html", context={"job_id": job_id})
    else:
        return render(request, "page_cnv_recom_en.html", context={"job_id": job_id})


def home_met(request):

    job_id = f"{datetime.strftime(datetime.now(), '%Y-%m-%d')}_{uuid1()}"

    if request.GET.get("lang") == "cn":
        return render(request, "page_met.html", context={"job_id": job_id})
    else:
        return render(request, "page_met_en.html", context={"job_id": job_id})


def analyze_met(request):

    print(123123)

    job_id = request.POST.get("job_id")
    name = request.POST.get("output")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    # 生成分析命令
    cmd = f"perl /home/cnv_user/met_test/script/pipline.pl " \
          f"-gene {path}/case.gene.xls -bam {path}/case.bam -outdir {path}/ -sample {name}"

    with open(f"{path}/cmd.sh", "w") as fw:
        fw.write(f"{cmd}")
    print(cmd)

    subprocess.check_call(cmd, shell=True)

    df_rslt = pd.read_csv(f"{path}/{name}.met.xls", sep="\t")
    response = {"code": 0, "msg": "", "count": df_rslt.shape[0], "data": df_rslt.to_dict(orient="records")}

    # 删除目录
    for file in glob(f"{path}/*"):
        if os.path.basename(file) != f"{name}.met.xls":
            subprocess.call(f"rm {file}", shell=True)

    return response_json(response=response, default=str)


def analyze(request):

    job_id = request.POST.get("job_id")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    # 生成分析命令
    cmd = f"/home/cnv_user/anaconda3/bin/python " \
          f"/home/cnv_user/software/CNVrecom/CNVrecom-main.py " \
          f"-c {path}/case.bam " \
          f"-n {path}/control.bam " \
          f"-t {path}/chip.bed " \
          f" {request.POST.dict().get('args')} " \
          f"-o {path}/CNVrecomReport.tsv"

    with open(f"{path}/cmd.sh", "w") as fw:
        fw.write(f"{cmd}")
    print(cmd)

    subprocess.check_call(cmd, shell=True)

    df_rslt = pd.read_csv(f"{path}/CNVrecomReport.tsv", sep="\t")
    response = {"code": 0, "msg": "", "count": df_rslt.shape[0], "data": df_rslt.to_dict(orient="records")}

    # 删除目录
    for file in glob(f"{path}/*"):
        if os.path.basename(file) != "CNVrecomReport.tsv":
            subprocess.call(f"rm {file}", shell=True)

    return response_json(response=response, default=str)


def upload(request):
    """上传input结果"""

    # 创建临时目录
    job_id = request.POST.get("job_id")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    if not os.path.exists(path):
        os.makedirs(path)

    file = request.FILES['file']
    with open(f"{path}/input.zip", "wb") as fw:
        for chunk in file.chunks():
            fw.write(chunk)

    subprocess.check_call(f"unzip {path}/input.zip -d {path}/", shell=True)

    response = {"code": 0, "msg": ""}
    return response_json(response=json.dumps(response), default=str)


def download_demo(request):
    """下载文件"""

    file = open(f"{settings.STATIC_ROOT}/demo/demo_met.zip", 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="demo.zip"'
    return response


def upload_met_bam(request):
    """上传input结果"""

    # 创建临时目录
    job_id = request.POST.get("job_id")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    if not os.path.exists(path):
        os.makedirs(path)

    file = request.FILES['file']
    print(f"{path}/case.bam")
    with open(f"{path}/case.bam", "wb") as fw:
        for chunk in file.chunks():
            fw.write(chunk)

    response = {"code": 0, "msg": ""}
    return response_json(response=json.dumps(response), default=str)


def upload_met_bai(request):
    """上传input结果"""

    # 创建临时目录
    job_id = request.POST.get("job_id")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    if not os.path.exists(path):
        os.makedirs(path)

    file = request.FILES['file']
    print(f"{path}/case.bam.bai")
    with open(f"{path}/case.bam.bai", "wb") as fw:
        for chunk in file.chunks():
            fw.write(chunk)

    response = {"code": 0, "msg": ""}
    return response_json(response=json.dumps(response), default=str)


def upload_met_gene(request):
    """上传input结果"""

    # 创建临时目录
    print(1231312)
    job_id = request.POST.get("job_id")
    path = f"{settings.ANALYZE_ROOT}/{job_id}"

    if not os.path.exists(path):
        os.makedirs(path)

    file = request.FILES['file']
    print(f"{path}/case.gene.xls")
    with open(f"{path}/case.gene.xls", "wb") as fw:
        for chunk in file.chunks():
            fw.write(chunk)

    response = {"code": 0, "msg": ""}
    return response_json(response=json.dumps(response), default=str)
