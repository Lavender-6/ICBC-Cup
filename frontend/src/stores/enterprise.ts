import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Enterprise, Valuation, TeamPortrait, PatentNetwork } from '@/api/enterprise'

export const useEnterpriseStore = defineStore('enterprise', () => {
  const currentEnterprise = ref<Enterprise | null>(null)
  const valuation = ref<Valuation | null>(null)
  const teamPortrait = ref<TeamPortrait | null>(null)
  const patentNetwork = ref<PatentNetwork | null>(null)

  function setEnterprise(enterprise: Enterprise) {
    currentEnterprise.value = enterprise
    valuation.value = null
    teamPortrait.value = null
    patentNetwork.value = null
  }

  function setValuation(v: Valuation) {
    valuation.value = v
  }

  function setTeam(t: TeamPortrait) {
    teamPortrait.value = t
  }

  function setPatents(p: PatentNetwork) {
    patentNetwork.value = p
  }

  return {
    currentEnterprise,
    valuation,
    teamPortrait,
    patentNetwork,
    setEnterprise,
    setValuation,
    setTeam,
    setPatents,
  }
})
