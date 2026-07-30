{{- define "nexus.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nexus.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- include "nexus.name" . -}}
{{- end -}}
{{- end -}}

{{- define "nexus.imageTag" -}}
{{- $tag := default .Chart.AppVersion .Values.image.tag -}}
{{- if or (eq $tag "") (eq $tag "local") -}}
{{- fail "A deployable image tag is required: package the chart with --app-version RELEASE_VERSION or set image.tag" -}}
{{- end -}}
{{- $tag -}}
{{- end -}}

{{- define "nexus.versionLabel" -}}
{{- include "nexus.imageTag" . | replace "+" "_" | trunc 63 | trimSuffix "-_." -}}
{{- end -}}

{{- define "nexus.commonLabels" -}}
app.kubernetes.io/part-of: nexus-ai-observability
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | quote }}
app.kubernetes.io/version: {{ include "nexus.versionLabel" . | quote }}
{{- end -}}

{{- define "nexus.selectorLabels" -}}
app.kubernetes.io/name: {{ .component }}
app.kubernetes.io/instance: {{ .root.Release.Name }}
{{- end -}}
