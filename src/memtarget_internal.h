/*
 *
 * Copyright (C) 2023-2024 Intel Corporation
 *
 * Under the Apache License v2.0 with LLVM Exceptions. See LICENSE.TXT.
 * SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
 *
 */

#ifndef UMF_MEMTARGET_INTERNAL_H
#define UMF_MEMTARGET_INTERNAL_H 1

#include <umf/base.h>
#include <umf/memtarget.h>
#ifdef __cplusplus
extern "C" {
#endif

struct umf_memtarget_ops_t;
typedef struct umf_memtarget_ops_t umf_memtarget_ops_t;

typedef struct umf_memtarget_t {
    const umf_memtarget_ops_t *ops;
    void *priv;
} umf_memtarget_t;

umf_result_t umfMemtargetCreate(const umf_memtarget_ops_t *ops, void *params,
                                umf_memtarget_handle_t *memoryTarget);
void umfMemtargetDestroy(umf_memtarget_handle_t memoryTarget);

umf_result_t umfMemtargetClone(umf_memtarget_handle_t memoryTarget,
                               umf_memtarget_handle_t *outHandle);

umf_result_t umfMemtargetGetBandwidth(umf_memtarget_handle_t srcMemoryTarget,
                                      umf_memtarget_handle_t dstMemoryTarget,
                                      size_t *bandwidth);
umf_result_t umfMemtargetGetLatency(umf_memtarget_handle_t srcMemoryTarget,
                                    umf_memtarget_handle_t dstMemoryTarget,
                                    size_t *latency);

#ifdef __cplusplus
}
#endif

#endif /* UMF_MEMTARGET_INTERNAL_H */
